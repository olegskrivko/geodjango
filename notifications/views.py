import json
from django.conf import settings
import logging
from pywebpush import webpush, WebPushException
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PushSubscription
from .serializers import PushSubscriptionSerializer
vapid_private_key = settings.WEBPUSH_SETTINGS.get("VAPID_PRIVATE_KEY")

logger = logging.getLogger(__name__)

VAPID_PRIVATE_KEY = f"{vapid_private_key}"

class PushSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = PushSubscription.objects.all()
    serializer_class = PushSubscriptionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Public read, auth required for write

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request):
        """
        Save or update a push subscription for the authenticated user.
        """
        subscription_data = request.data
        endpoint = subscription_data.get('endpoint')
        p256dh = subscription_data.get('p256dh')
        auth = subscription_data.get('auth')
        lat = subscription_data.get('lat', 56.946)
        lon = subscription_data.get('lon', 24.1059)
        distance = subscription_data.get('distance', 200.0)

        if not endpoint or not p256dh or not auth:
            return Response({"error": "Missing subscription data."}, status=status.HTTP_400_BAD_REQUEST)

        subscription, created = PushSubscription.objects.update_or_create(
            user=request.user,
            endpoint=endpoint,
            defaults={
                'p256dh': p256dh,
                'auth': auth,
                'lat': lat,
                'lon': lon,
                'distance': distance,
            }
        )

        return Response(
            {"message": "Subscription saved!" if created else "Subscription updated."},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def unsubscribe(self, request):
        """
        Remove a push subscription for the authenticated user.
        """
        subscription_data = request.data
        try:
            subscription = PushSubscription.objects.get(endpoint=subscription_data['endpoint'], user=request.user)
            subscription.delete()
            return Response({"message": "Unsubscribed successfully!"}, status=status.HTTP_200_OK)
        except PushSubscription.DoesNotExist:
            return Response({"detail": "Subscription not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def send_notification(self, request):
        """
        Send a push notification to all subscriptions of the authenticated user.
        """
        data = request.data
        title = data.get('title')
        body = data.get('body')
        url = data.get('url', '/')

        if not all([title, body]):
            return Response({"error": "Missing required fields: title and body"}, status=status.HTTP_400_BAD_REQUEST)

        subscriptions = PushSubscription.objects.filter(user=request.user)
        if not subscriptions:
            return Response({"error": "No subscriptions found for this user"}, status=status.HTTP_404_NOT_FOUND)

        payload = json.dumps({
            "title": title,
            "body": body,
            "url": url,
            "icon": data.get("icon", f"{settings.DOMAIN_APP_URL}/static/logo192.png"),
            "badge": data.get("badge", f"{settings.DOMAIN_APP_URL}/static/logo192.png"),
            "image": data.get("image"),  # optional, can be None
            "actions": data.get("actions", [
                {"action": "open", "title": "View Pet"},
                {"action": "close", "title": "Close"}
            ]),
            "data": data.get("data", {})  # additional custom data
        })

        failures = []
        for subscription in subscriptions:
            try:
                logger.info(f"Sending push notification to {subscription.endpoint}")
                webpush(
                    subscription_info={
                        "endpoint": subscription.endpoint,
                        "keys": {
                            "p256dh": subscription.p256dh,
                            "auth": subscription.auth
                        }
                    },
                    data=payload,
                    vapid_private_key=settings.WEBPUSH_SETTINGS['VAPID_PRIVATE_KEY'],
                    vapid_claims={
                        "sub": f"mailto:{settings.WEBPUSH_SETTINGS['VAPID_ADMIN_EMAIL']}"
                    }
                )
            except WebPushException as ex:
                logger.error(f"Push failed for endpoint {subscription.endpoint}: {str(ex)}")
                failures.append(subscription.endpoint)

        if failures:
            return Response({
                "error": "Some notifications failed.",
                "failed_endpoints": failures
            }, status=status.HTTP_207_MULTI_STATUS)

        return Response({"message": "Notification sent successfully!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def is_subscribed(self, request):
        """
        Check if the current user is subscribed to a specific endpoint.
        """
        endpoint = request.query_params.get("endpoint")
        if not endpoint:
            return Response({"error": "Missing 'endpoint' query param."}, status=status.HTTP_400_BAD_REQUEST)

        exists = PushSubscription.objects.filter(user=request.user, endpoint=endpoint).exists()
        return Response({"subscribed": exists}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='user-location')
    def user_location(self, request):
        """
        Return the most recent PushSubscription's location for the current user.
        """
        subscription = (
            PushSubscription.objects.filter(user=request.user)
            .order_by('-created_at')
            .first()
        )

        if subscription:
            data = {
                'lat': subscription.lat,
                'lon': subscription.lon,
                'distance': subscription.distance,
            }
        else:
            data = {
                'lat': 56.946285,
                'lon': 24.105078,
                'distance': 5.0,
            }

        return Response(data, status=status.HTTP_200_OK)