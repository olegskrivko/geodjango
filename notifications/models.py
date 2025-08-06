from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PushSubscription(models.Model):
    # ForeignKey to User to associate subscriptions with users
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    # The endpoint is the unique URL provided by the browser's push service. It is used to send push notifications to the correct device/browser instance.
    # endpoint = models.URLField()
    endpoint = models.URLField(max_length=1000)  # increased from default 200 to 1000
    # The p256dh field stores the user's public key for the push subscription. It is used for encrypting the payload of push messages, ensuring that only the intended client can decrypt the notification.
    p256dh = models.CharField(max_length=255)
    # The auth field stores the authentication secret for the push subscription. It is used as part of the encryption process to authenticate the push messages and prevent unauthorized parties from sending notifications.
    auth = models.CharField(max_length=255)
    # The lat field stores the latitude of the user's location, which can be used to send location-based notifications (e.g., alerts about nearby events or services).
    lat = models.FloatField(default=56.946)
    # The lon field stores the longitude of the user's location, complementing the latitude for precise geolocation-based notifications.
    lon = models.FloatField(default=24.1059)
    # The distance field defines the radius (in kilometers) for which the user wants to receive notifications, enabling personalized, location-based notification delivery.
    distance = models.FloatField(default=5.0)
    # The created_at field records when the subscription was created, which can be useful for managing and expiring old subscriptions.
    created_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Subscription for {self.user.username} at {self.lat}, {self.lon} within {self.distance} km"

    class Meta:
        unique_together = ('user', 'endpoint')  # Ensure a user can have only one subscription per endpoint
