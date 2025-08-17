# services/views.py
from rest_framework import serializers
from rest_framework import viewsets, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Service,  Review, WorkingHour, Location 
from .serializers import ServiceSerializer, ReviewSerializer
import cloudinary.uploader
from rest_framework import status
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .filters import ServiceFilter
# Add this at the top if you haven't already
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as filters
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
import django_filters
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
import json
from .models import Service, Location, ServiceView, ServiceShare, ServiceReport, WorkingHour
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.db.models import Count
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import OuterRef, Subquery, Value, FloatField
from django.db.models import Min
from django.db.models import Prefetch
from django.db.models import OuterRef, Subquery, Min, F
from django.db.models.functions import Coalesce
from django.db import models
from django.db.models import F, ExpressionWrapper
User = get_user_model()

class ServicePagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'totalPages': self.page.paginator.num_pages,
            'currentPage': self.page.number,
            'results': data
        })

class ServiceFilter(filters.FilterSet):
    category = filters.NumberFilter(field_name='category', lookup_expr='exact')
    provider = filters.NumberFilter(field_name='provider', lookup_expr='exact')
    search = filters.CharFilter(method='filter_by_search', label='Search')

    def filter_by_search(self, queryset, name, value):
        """Split the search string into separate terms. Allow searching on operating name and description"""
        terms = value.strip().split()
        for term in terms:
            queryset = queryset.filter(
                Q(description__icontains=term) | Q(operating_name__icontains=term)
            )
        return queryset

    class Meta:
        model = Service
        fields = ['search', 'category', 'provider']

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all().order_by('-created_at')
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ServiceFilter
    pagination_class = ServicePagination
    parser_classes = (MultiPartParser, FormParser)
    ordering_fields = ['created_at', 'price', 'rating', 'distance']

    def get_service_limit(self, user):
        if getattr(user, "is_subscribed", False):
            if getattr(user, "subscription_type", "") == 'plus':
                return 3
            elif getattr(user, "subscription_type", "") == 'premium':
                return 5
        return 2
    
    def create(self, request, *args, **kwargs):
        # 1️⃣ Parse locations from JSON string
        raw_locations = request.data.get("locations", "[]")
        try:
            locations_data = json.loads(raw_locations)
        except json.JSONDecodeError:
            raise ValidationError({"locations": "Invalid JSON format for locations."})

        # 2️⃣ Validate main service fields
        mutable_data = request.data.copy()
        mutable_data.setlist("locations", [])  # Clear locations for serializer
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)

        # 3️⃣ Let the serializer handle the complete creation (service + locations)
        # The serializer will get locations from context and create everything
        service = serializer.save(user=request.user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer, locations_data):
        user = self.request.user
        service_limit = self.get_service_limit(user)
        if Service.objects.filter(user=user).count() >= service_limit:
            raise ValidationError(
                f"You have reached your service posting limit ({service_limit})."
            )

        # 1️⃣ Handle images
        uploaded_images = {}
        uploaded_images_list = []
        for i in range(1, 5):
            image_field = f"service_image_{i}_media"
            image = self.request.FILES.get(image_field)
            if image:
                uploaded_image = cloudinary.uploader.upload(image)
                uploaded_images_list.append(uploaded_image.get("secure_url"))

        if not uploaded_images_list:
            raise ValidationError({"error": "At least one image must be uploaded."})

        # Map images to service fields
        for idx, url in enumerate(uploaded_images_list):
            uploaded_images[f"service_image_{idx+1}"] = url
        for idx in range(len(uploaded_images_list) + 1, 5):
            uploaded_images[f"service_image_{idx}"] = None

        # 2️⃣ Save the Service instance with images
        # The serializer will handle location creation
        service = serializer.save(user=user, **uploaded_images)
        
        return service

    def get_queryset(self):
        queryset = super().get_queryset()

        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        latitude = 56.9496
        longitude = 24.1052

        if latitude and longitude:
            try:
                user_point = Point(float(longitude), float(latitude), srid=4326)

                # Subquery to calculate min distance per service
                min_distance_subquery = (Location.objects.filter(service=OuterRef('pk')).annotate(distance=Distance('location', user_point)).values('service').annotate(min_distance=Min('distance')).values('min_distance'))

                queryset = (
                    queryset.annotate(min_distance_km=Coalesce(Subquery(min_distance_subquery, output_field=FloatField()) / 1000.0, 99999.0)).order_by('min_distance_km').prefetch_related(Prefetch('locations', queryset=Location.objects.annotate(distance=Distance('location', user_point)).order_by('distance')))
                )

            except (ValueError, TypeError):
                pass

        return queryset

    # def get_queryset(self):
    #         queryset = super().get_queryset()

    #         latitude = self.request.query_params.get('latitude')
    #         longitude = self.request.query_params.get('longitude')
    #         latitude = 56.9496
    #         longitude = 24.1052

    #         if latitude and longitude:
    #             try:
    #                 user_point = Point(float(longitude), float(latitude), srid=4326)

    #                 # Annotate distance on Location queryset
    #                 locations_with_distance = Location.objects.annotate(
    #                     distance=Distance('location', user_point)
    #                 ).order_by('distance')

    #                 # Prefetch annotated locations in services queryset
    #                 queryset = queryset.prefetch_related(
    #                     Prefetch('locations', queryset=locations_with_distance)
    #                 )
    #             except (ValueError, TypeError):
    #                 pass  # Ignore bad input, fallback to no distance annotation

    #         return queryset
 


  



    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    # def create(self, request, *args, **kwargs):
    #     print("Received request data:", request.data)

    #     # Step 1: Handle and extract location string → Python list
    #     raw_locations = request.data.get("locations")
    #     if isinstance(raw_locations, list):
    #         raw_locations = raw_locations[0]  # because QueryDict stores it as list
    #     try:
    #         parsed_locations = json.loads(raw_locations) if raw_locations else []
    #     except json.JSONDecodeError:
    #         raise ValidationError({"locations": "Invalid JSON format for locations."})

    #     # Step 2: Copy request data and manually inject parsed locations
    #     mutable_data = request.data.copy()
    #     mutable_data.setlist("locations", [])  # wipe it to avoid confusion
    #     serializer = self.get_serializer(data=mutable_data)
    #     serializer.is_valid(raise_exception=True)

    #     # Step 3: save and pass locations + images to perform_create
    #     self.perform_create(serializer, parsed_locations)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def perform_create(self, serializer, locations_data):
    #     user = self.request.user
    #     current_count = Service.objects.filter(user=user).count()
    #     service_limit = self.get_service_limit(user)
    #     if current_count >= service_limit:
    #         raise ValidationError(f"You have reached your service posting limit ({service_limit}). Please delete an existing service or upgrade your subscription.")
    #     print("hello from perform_create", locations_data)

    #     uploaded_images = {}
    #     uploaded_images_list = []

    #     for i in range(1, 5):
    #         image_field = f"service_image_{i}_media"
    #         image = self.request.FILES.get(image_field)
    #         if image:
    #             uploaded_image = cloudinary.uploader.upload(image)
    #             uploaded_images_list.append(uploaded_image.get("secure_url"))

    #     if not uploaded_images_list:
    #         raise ValidationError({"error": "At least one image must be uploaded."})

    #     for index, image_url in enumerate(uploaded_images_list):
    #         uploaded_images[f"service_image_{index+1}"] = image_url
    #     for i in range(len(uploaded_images_list) + 1, 5):
    #         uploaded_images[f"service_image_{i}"] = None

    #     service = serializer.save(user=self.request.user, **uploaded_images)

    #     # Create related location objects with correct field mapping
    #     for loc in locations_data:
    #         if not all(k in loc for k in ("title", "description", "lat", "lng", "region", "city", "street", "postal_code", "full_address" )):
    #             raise ValidationError({"locations": "Each location must include title, description, lat, and lng."})
            
    #         try:
    #             lat = float(loc["lat"])
    #             lng = float(loc["lng"])
    #         except ValueError:
    #             raise ValidationError({"locations": "Latitude and Longitude must be valid numbers."})

    #         location = Location.objects.create(
    #             service=service,
    #             location_title=loc["title"],
    #             location_description=loc["description"],
    #             latitude=lat,
    #             longitude=lng,
    #             region=loc["region"],
    #             city=loc["city"],
    #             street=loc["street"],
    #             postal_code=loc["postal_code"],
    #             full_address=loc["full_address"],
    #         )

    #         # Create default working hours for each location (Monday to Friday, 9:00-17:00)
    #         from datetime import time
    #         default_working_hours = [
    #             (0, time(9, 0), time(17, 0)),  # Monday
    #             (1, time(9, 0), time(17, 0)),  # Tuesday
    #             (2, time(9, 0), time(17, 0)),  # Wednesday
    #             (3, time(9, 0), time(17, 0)),  # Thursday
    #             (4, time(9, 0), time(17, 0)),  # Friday
    #             # Saturday and Sunday are not created (weekend)
    #         ]
            
    #         for day, from_hour, to_hour in default_working_hours:
    #             WorkingHour.objects.create(
    #                 location=location,
    #                 day=day,
    #                 from_hour=from_hour,
    #                 to_hour=to_hour
    #             )

    def retrieve(self, request, pk=None):
        service = self.get_object()

        # Track the view (only once per user/IP per day)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        user = request.user if request.user.is_authenticated else None

        from django.utils import timezone
        from datetime import timedelta

        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)

        existing_view = None
        if user:
            existing_view = ServiceView.objects.filter(
                service=service,
                user=user,
                created_at__gte=today_start,
                created_at__lt=today_end
            ).first()
        else:
            existing_view = ServiceView.objects.filter(
                service=service,
                ip_address=ip_address,
                created_at__gte=today_start,
                created_at__lt=today_end
            ).first()

        if not existing_view:
            ServiceView.objects.create(
                service=service,
                user=user,
                ip_address=ip_address if not user else None
            )

        serializer = self.get_serializer(service)
        return Response(serializer.data)

class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get user coordinates from query parameters
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        
        if latitude and longitude:
            try:
                user_location = Point(float(longitude), float(latitude), srid=4326)
                
                # Subquery to get minimum distance to user's point among related locations
                min_distance_subquery = Location.objects.filter(
                    service=OuterRef('pk'),
                    location__isnull=False
                ).annotate(
                    dist=Distance('location', user_location)
                ).order_by('dist').values('dist')[:1]

                # Annotate services with that minimum distance
                queryset = queryset.annotate(
                    min_distance=Subquery(min_distance_subquery, output_field=FloatField())
                )
                
            except (ValueError, TypeError):
                pass

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        
        # Get user coordinates from query parameters
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        
        if latitude and longitude:
            try:
                context['user_point'] = Point(float(longitude), float(latitude), srid=4326)
            except (ValueError, TypeError):
                pass
        return context


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return Review.objects.filter(service_id=service_id)

    def perform_create(self, serializer):
        user = self.request.user
        service_id = self.kwargs['service_id']
        service = Service.objects.get(id=service_id)

        # Check if the review already exists
        existing_review = Review.objects.filter(user=user, service=service).first()

        if existing_review:
            # Update existing review with validated data
            existing_review.rating = serializer.validated_data['rating']
            existing_review.comment = serializer.validated_data['comment']
            existing_review.save()
        else:
            # Create a new review using serializer (which already has validated data)
            serializer.save(user=user, service=service)





@api_view(['GET'])
@permission_classes([AllowAny])
def service_view_stats(request, service_id):
    """
    Get view statistics for a specific service.
    Anyone can view these stats.
    """
    print(f"DEBUG: service_view_stats called for service_id: {service_id}")
    try:
        service = Service.objects.get(id=service_id)
        print(f"DEBUG: Found service: {service.id}")
        
        # Get all views for this service
        all_views = ServiceView.objects.filter(service=service)
        all_shares = ServiceShare.objects.filter(service=service)
        print(f"DEBUG: Found {all_views.count()} views and {all_shares.count()} shares")
        
        # Calculate statistics
        total_views = all_views.count()
        total_shares = all_shares.count()
        
        # Unique views (by user or IP)
        unique_views = all_views.values('user', 'ip_address').distinct().count()
        unique_shares = all_shares.values('user', 'ip_address').distinct().count()
        
        # Recent views (last 7 days)
        from django.utils import timezone
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        recent_views = all_views.filter(created_at__gte=week_ago).count()
        recent_shares = all_shares.filter(created_at__gte=week_ago).count()
        
        # Views by day (last 7 days)
        daily_views = []
        daily_shares = []
        for i in range(7):
            date = timezone.now() - timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            count = all_views.filter(created_at__gte=day_start, created_at__lt=day_end).count()
            share_count = all_shares.filter(created_at__gte=day_start, created_at__lt=day_end).count()
            daily_views.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': count
            })
            daily_shares.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': share_count
            })
        daily_views.reverse()  # Show oldest to newest
        daily_shares.reverse()
        
        # Share methods breakdown
        share_methods = all_shares.values('method').annotate(count=Count('method')).order_by('-count')
        print(f"DEBUG: Returning stats - views: {total_views}, shares: {total_shares}")
        
        return Response({
            'service_id': service_id,
            'total_views': total_views,
            'unique_views': unique_views,
            'recent_views': recent_views,
            'daily_views': daily_views,
            'total_shares': total_shares,
            'unique_shares': unique_shares,
            'recent_shares': recent_shares,
            'daily_shares': daily_shares,
            'share_methods': share_methods
        })
        
    except Service.DoesNotExist:
        print(f"DEBUG: Service not found with ID: {service_id}")
        return Response(
            {"error": "Service not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def track_service_share(request, service_id):
    """
    Track when a service is shared.
    """
    print(f"DEBUG: track_service_share called for service_id: {service_id}")
    print(f"DEBUG: Request data: {request.data}")
    print(f"DEBUG: Request user: {request.user}")
    print(f"DEBUG: Request META: {dict(request.META)}")
    
    try:
        service = Service.objects.get(id=service_id)
        print(f"DEBUG: Found service: {service.id}")
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        print(f"DEBUG: Detected IP: {ip}")
        
        # Get share method from request data
        share_method = request.data.get('method', 'unknown')  # e.g., 'facebook', 'twitter', 'copy_link', etc.
        print(f"DEBUG: Share method: {share_method}")
        
        # Check if this user/IP has already shared this service today
        from django.utils import timezone
        from datetime import timedelta
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # Check for existing share today
        existing_share = None
        if request.user.is_authenticated:
            # For authenticated users, check by user
            existing_share = ServiceShare.objects.filter(
                service=service,
                user=request.user,
                method=share_method,
                created_at__gte=today_start,
                created_at__lt=today_end
            ).first()
        else:
            # For anonymous users, check by IP
            existing_share = ServiceShare.objects.filter(
                service=service,
                ip_address=ip,
                method=share_method,
                created_at__gte=today_start,
                created_at__lt=today_end
            ).first()
        
        # Only create a new share record if no share exists for today with this method
        if not existing_share:
            print(f"DEBUG: Creating ServiceShare record...")
            share_record = ServiceShare.objects.create(
                service=service,
                user=request.user if request.user.is_authenticated else None,
                ip_address=ip if not request.user.is_authenticated else None,
                method=share_method
            )
            print(f"DEBUG: Created share record with ID: {share_record.id}")
        else:
            print(f"DEBUG: Share already tracked today for this user/IP and method")
        
        return Response({
            'service_id': service_id,
            'method': share_method,
            'message': 'Share tracked successfully' if not existing_share else 'Share already tracked today'
        })
        
    except Service.DoesNotExist:
        print(f"DEBUG: Service not found with ID: {service_id}")
        return Response(
            {"error": "Service not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        print(f"DEBUG: Error creating share record: {str(e)}")
        return Response(
            {"error": f"Error tracking share: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def flag_service(request, service_id):
    """
    Flag a service for inappropriate content.
    Requires authentication.
    """
    try:
        service = Service.objects.get(id=service_id)
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Check if user has already flagged this service
        existing_flag = ServiceReport.objects.filter(
            service=service,
            user=request.user
        ).first()
        
        if existing_flag:
            return Response(
                {"error": "You have already flagged this service."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the flag
        flag = ServiceReport.objects.create(
            service=service,
            user=request.user,
            ip_address=ip
        )
        
        # Check if service should be banned (5 or more unique flags)
        unique_flags_count = ServiceReport.objects.filter(service=service).count()
        
        if unique_flags_count >= 5:
            # Ban the service
            service.is_banned = True
            service.save()
            
            return Response({
                'service_id': service_id,
                'message': 'Service flagged successfully. Service has been banned due to multiple flags.',
                'banned': True,
                'flag_count': unique_flags_count
            })
        else:
            return Response({
                'service_id': service_id,
                'message': 'Service flagged successfully.',
                'banned': False,
                'flag_count': unique_flags_count
            })
        
    except Service.DoesNotExist:
        return Response(
            {"error": "Service not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Error flagging service: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unflag_service(request, service_id):
    """
    Remove flag from a service.
    Requires authentication.
    """
    try:
        service = Service.objects.get(id=service_id)
        
        # Find and delete the user's flag
        flag = ServiceReport.objects.filter(
            service=service,
            user=request.user
        ).first()
        
        if not flag:
            return Response(
                {"error": "You have not flagged this service."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        flag.delete()
        
        # Check if service should be unbanned (less than 5 flags now)
        unique_flags_count = ServiceReport.objects.filter(service=service).count()
        
        if unique_flags_count < 5 and service.is_banned:
            # Unban the service
            service.is_banned = False
            service.save()
            
            return Response({
                'service_id': service_id,
                'message': 'Flag removed successfully. Service has been unbanned.',
                'banned': False,
                'flag_count': unique_flags_count
            })
        else:
            return Response({
                'service_id': service_id,
                'message': 'Flag removed successfully.',
                'banned': unique_flags_count >= 5 and service.is_banned,
                'flag_count': unique_flags_count
            })
        
    except Service.DoesNotExist:
        return Response(
            {"error": "Service not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Error removing flag: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_service_flag_status(request, service_id):
    """
    Get the flag status for the current user and total flag count.
    """
    try:
        service = Service.objects.get(id=service_id)
        
        # Check if current user has flagged this service
        user_flagged = ServiceReport.objects.filter(
            service=service,
            user=request.user
        ).exists()
        
        # Get total flag count
        total_flags = ServiceReport.objects.filter(service=service).count()
        
        # Only consider banned if it has 5+ flags AND is banned
        is_banned_by_flags = total_flags >= 5 and service.is_banned
        
        return Response({
            'service_id': service_id,
            'user_flagged': user_flagged,
            'total_flags': total_flags,
            'banned': is_banned_by_flags
        })
        
    except Service.DoesNotExist:
        return Response(
            {"error": "Service not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )

# Limits per subscription type
SUBSCRIPTION_LIMITS = {
    'free': 3,
    'plus': 5,
    'premium': 7,
}

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def service_post_quota(request):
    user = request.user

    # Default to 'free' if no subscription
    subscription_type = getattr(user, 'subscription_type', 'free')
    service_limit = SUBSCRIPTION_LIMITS.get(subscription_type, SUBSCRIPTION_LIMITS['free'])

    current_count = Service.objects.filter(user=user).count()
    remaining = max(service_limit - current_count, 0)

    return Response({
        'limit': service_limit,
        'used': current_count,
        'remaining': remaining,
        'subscription_type': subscription_type
    })

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def service_post_quota(request):
#     user = request.user
#     service_limit = 1
#     if getattr(user, "is_subscribed", False):
#         if user.subscription_type == 'plus':
#             service_limit = 3
#         elif user.subscription_type == 'premium':
#             service_limit = 5
#     current_count = Service.objects.filter(user=user).count()
#     remaining = max(service_limit - current_count, 0)
#     return Response({
#         'limit': service_limit,
#         'used': current_count,
#         'remaining': remaining
#     })
