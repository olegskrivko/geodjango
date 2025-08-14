from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pet, PetSightingHistory, PetView, PetShare, PetReport
from .serializers import PetSerializer, PetSightingHistorySerializer, PosterSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, permissions
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
#from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from django.db.models import OuterRef, Subquery
from django.db.models import Q
from django.utils.timezone import make_aware
from datetime import datetime
from django.utils import timezone
import django_filters
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# from django.contrib.auth.models import User
from decimal import Decimal, InvalidOperation
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from decimal import Decimal
from django.utils.timezone import now
from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary.uploader
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from django_filters import DateFilter
# from .models import PushSubscription
from math import radians, sin, cos, sqrt, atan2
from django.http import JsonResponse
from django.conf import settings
from notifications.models import PushSubscription
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from pets.models import Poster
import json
from rest_framework import generics
from django.db.models import Count
from rest_framework.parsers import JSONParser
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D  # "D" stands for Distance
from django.contrib.gis.db.models import GeometryField
from notifications.utils import send_push_notification  # Import the push notification function
from django.contrib.gis.db import models as geomodels

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Difference in coordinates
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance
User = get_user_model()


class PetFilter(filters.FilterSet):
    status = filters.NumberFilter(field_name='status', lookup_expr='exact')
    species = filters.NumberFilter(field_name='species', lookup_expr='exact') 
    age = filters.NumberFilter(field_name='age', lookup_expr='exact')
    gender = filters.NumberFilter(field_name='gender', lookup_expr='exact')
    size = filters.NumberFilter(field_name='size', lookup_expr='exact')
    pattern = filters.NumberFilter(field_name='pattern', lookup_expr='exact')
    date = DateFilter(field_name='event_occurred_at', lookup_expr='gte')
    color = filters.NumberFilter(method='filter_by_color')
    search = filters.CharFilter(method='filter_by_search', label='Search')
    
    def filter_by_color(self, queryset, name, value):
        """ Filter pets by either primary_color or secondary_color matching the selected color """
        return queryset.filter(
            Q(primary_color=value) | Q(secondary_color=value)
        )
    
    def filter_by_search(self, queryset, name, value):
        """Split the search string into separate terms. Allow searching on name and notes"""
        terms = value.strip().split()
        for term in terms:
            queryset = queryset.filter(
                Q(notes__icontains=term) | Q(breed__icontains=term)
            )
        return queryset
    
    class Meta:
        model = Pet
        fields = ['search', 'species', 'age', 'gender', 'size', 'status', 'pattern', 'date', 'color']


@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def get_user_pets(request):
    """
    Fetch all pets created by the logged-in user.
    """
    print(request)
    user = request.user  # Get the logged-in user
    print(request)
    pets = Pet.objects.filter(author=user)
    serializer = PetSerializer(pets, many=True)
    return Response(serializer.data)



class UserPostersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        posters = Poster.objects.filter(pet__author=user)
        serializer = PosterSerializer(posters, many=True)
        return Response(serializer.data)
# class UserPostersListView(generics.ListAPIView):
#     serializer_class = PosterSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get_queryset(self):
#         user = self.request.user
#         return Poster.objects.filter(pet__author=user)
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_posters(request):
#     """
#     Return all posters created for pets owned by the current user.
#     """
#     user = request.user
#     posters = Poster.objects.filter(pet__author=user)
#     serializer = PosterSerializer(posters, many=True)
#     return Response(serializer.data)

# class PosterBulkCreateView(APIView):
#     permission_classes = [IsAuthenticated]  # ✅ Require login

#     def post(self, request):
#         pet_id = request.data.get('pet')
#         name = request.data.get('name', '')
#         count = int(request.data.get('count', 1))

#         # ✅ Check if pet exists and is owned by current user
#         pet = get_object_or_404(Pet, id=pet_id)
#         if pet.author != request.user:
#             return Response(
#                 {"error": "You can only create posters for your own pets."},
#                 status=status.HTTP_403_FORBIDDEN
#             )

#         posters = []
#         for i in range(count):
#             poster_name = f"{name} #{i+1}" if count > 1 else name
#             poster = Poster.objects.create(
#                 pet=pet,  # Pass the Pet object, not just ID
#                 name=poster_name
#             )
#             posters.append({
#                 "id": str(poster.id),
#                 "pet": str(pet.id),
#                 "name": poster.name
#             })

#         return Response(posters, status=status.HTTP_201_CREATED)
# class PosterBulkCreateView(APIView):
#     permission_classes = [IsAuthenticated]  # ✅ Require login

#     def post(self, request):
#         pet_id = request.data.get('pet')
#         name = request.data.get('name', '')
#         count = int(request.data.get('count', 1))

#         # ✅ Enforce a limit
#         if count < 1:
#             return Response({"error": "You must create at least 1 poster."}, status=status.HTTP_400_BAD_REQUEST)
#         if count > 20:
#             return Response({"error": "You can create a maximum of 20 posters at a time."}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ Check if pet exists and belongs to user
#         pet = get_object_or_404(Pet, id=pet_id)
#         if pet.author != request.user:
#             return Response({"error": "You can only create posters for your own pets."}, status=status.HTTP_403_FORBIDDEN)

#         posters = []
#         for i in range(count):
#             poster_name = f"{name} #{i+1}" if count > 1 else name
#             poster = Poster.objects.create(
#                 pet=pet,
#                 name=poster_name
#             )
#             posters.append({
#                 "id": str(poster.id),
#                 "pet": str(pet.id),
#                 "name": poster.name
#             })

#         return Response(posters, status=status.HTTP_201_CREATED)
class PosterBulkCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request):
        pet_id = request.data.get('pet')
        name = request.data.get('name', '')
        count = int(request.data.get('count', 1))

        posters = []
        for i in range(count):
            poster_name = f"{name} #{i+1}" if count > 1 else name
            poster = Poster.objects.create(
                pet_id=pet_id,
                name=poster_name
            )
            posters.append({
                "id": str(poster.id),
                "pet": pet_id,
                "name": poster.name
            })
        
        return Response(posters, status=status.HTTP_201_CREATED)

@csrf_exempt
def increment_poster_scan(request, poster_id):
    if request.method == 'POST':
        data = json.loads(request.body or "{}")

        try:
            poster = Poster.objects.get(id=poster_id)
        except Poster.DoesNotExist:
            return JsonResponse({"error": "Poster not found."}, status=404)

        if not poster.has_location and data.get("latitude") and data.get("longitude"):
            poster.latitude = data["latitude"]
            poster.longitude = data["longitude"]
            poster.has_location = True

        poster.scans += 1
        poster.save()

        return JsonResponse({
            "status": "ok",
            "scans": poster.scans,
            "pet_id": poster.pet_id
        })





class PetStatusCountsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        lost_count = Pet.objects.filter(status=1).count()
        found_count = Pet.objects.filter(status=2).count()
        seen_count = Pet.objects.filter(status=3).count()

        return Response({
            'lost': lost_count,
            'found': found_count,
            'seen': seen_count,
        })

class PetPagination(PageNumberPagination):
    page_size = 6  # Default page size
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Max number of items per page
    # You can override the `get_paginated_response` method if you want to customize the structure of the response.
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total number of pets
            'totalPages': self.page.paginator.num_pages,  # Total pages
            'currentPage': self.page.number,  # Current page number
            'results': data  # The paginated results
        })

    
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all().order_by('-created_at')  # Order by created_at in descending order (most recent first)
    serializer_class = PetSerializer
    
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow public read access, but auth required for write operations
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PetFilter
    pagination_class = PetPagination
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = super().get_queryset()

        # user defined coords
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')

        if latitude and longitude:
            try:
                user_location = Point(float(longitude), float(latitude), srid=4326)
                queryset = queryset.annotate(distance=Distance('location', user_location)).order_by('distance')
            except (ValueError, TypeError):
                pass  # Invalid input, ignore distance filtering

        return queryset
    
    # def get_pet_limit(self, user):
    #     if getattr(user, "is_subscribed", False):
    #         if getattr(user, "subscription_type", "") == 'plus':
    #             return 3
    #         elif getattr(user, "subscription_type", "") == 'premium':
    #             return 5
    #     return 1
  
    def list(self, request, *args, **kwargs):
        # The pagination logic is handled automatically by the pagination class
        return super().list(request, *args, **kwargs)
       
    def perform_create(self, serializer):
        user = self.request.user
        current_count = Pet.objects.filter(author=user).count()
        pet_limit = 5 

        if current_count >= pet_limit:
            raise ValidationError(
                f"You have reached the pet adding limit ({pet_limit}). "
                "Please delete an existing entry to add a new one."
            )
        # pet_limit = self.get_pet_limit(user)
        

        # if current_count >= pet_limit:
        #     raise ValidationError(
        #         f"Jūs esat sasniedzis mājdzīvnieku pievienošanas limitu ({pet_limit}). "
        #         "Lūdzu, dzēsiet esošu ierakstu vai atjauniniet abonementu."
        #     )

        uploaded_images = {}
        uploaded_images_list = []  # Store uploaded images in order

        # Handle image uploads (at least one required)
        for i in range(1, 5):  # Loop from pet_image_1 to pet_image_4
            image_field = f"pet_image_{i}_media"  # Field name from request
            image = self.request.FILES.get(image_field)

            if image:
                uploaded_image = cloudinary.uploader.upload(image)
                uploaded_images_list.append(uploaded_image.get("secure_url"))

        # Ensure at least one image is uploaded
        if not uploaded_images_list:
            raise ValidationError({"error": "At least one image must be uploaded."})

        # Assign images sequentially to pet_image_1, pet_image_2, etc.
        for index, image_url in enumerate(uploaded_images_list):
            uploaded_images[f"pet_image_{index+1}"] = image_url  # Assign in order

        # Fill remaining image fields with None
        for i in range(len(uploaded_images_list) + 1, 5):  # Ensure all 4 fields exist
            uploaded_images[f"pet_image_{i}"] = None
    
        date = self.request.data.get("date")  # e.g., "2025-04-01"
        time = self.request.data.get("time")  # e.g., "14:30"
        print("date", self.request.data.get("date"))

        if date and time:
            try:
                # Combine date and time into a single string
                combined_datetime_str = f"{date} {time}"
                # Parse the combined string into a datetime object
                event_occurred_at = datetime.strptime(combined_datetime_str, "%Y-%m-%d %H:%M")
                # Make it timezone-aware
                event_occurred_at = make_aware(event_occurred_at)
            except ValueError:
                event_occurred_at = timezone.now()  # Default to now if the date/time is invalid
        else:
            event_occurred_at = timezone.now()  # Default to now if missing

        pet = serializer.save(
            author=self.request.user,
         
            event_occurred_at=event_occurred_at,
             **uploaded_images  # Dynamically assign images
        )
        # Send notification if status is 'lost'
        if pet.status == 1:  # Or any other condition you want
            self.send_notifications_for_lost_pet(pet.id)

    def retrieve(self, request, pk=None):
        pet = get_object_or_404(Pet, pk=pk)
        
        # Track the view (only once per user/IP per day)
        ip_address = self.get_client_ip(request)
        user = request.user if request.user.is_authenticated else None
        
        # Check if this user/IP has already viewed this pet today
        from django.utils import timezone
        from datetime import timedelta
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # Check for existing view today
        existing_view = None
        if user:
            # For authenticated users, check by user
            existing_view = PetView.objects.filter(
                pet=pet,
                user=user,
                created_at__gte=today_start,
                created_at__lt=today_end
            ).first()
        else:
            # For anonymous users, check by IP
            existing_view = PetView.objects.filter(
                pet=pet,
                ip_address=ip_address,
                created_at__gte=today_start,
                created_at__lt=today_end
            ).first()
        
        # Only create a new view record if no view exists for today
        if not existing_view:
            PetView.objects.create(
                pet=pet,
                user=user,
                ip_address=ip_address if not user else None
            )
        
        serializer = self.get_serializer(pet)
        return Response(serializer.data)
    
    def get_client_ip(self, request):
        """Get the client's IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def update(self, request, pk=None):
        pet = get_object_or_404(Pet, pk=pk, author=request.user)
        serializer = self.get_serializer(pet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        pet = get_object_or_404(Pet, pk=pk, author=request.user)
        pet.delete()
        return Response({"message": "Pet deleted successfully."}, status=204)
    
    def send_notifications_for_lost_pet(self, pet_id):
        try:
            pet = Pet.objects.get(id=pet_id)
        except Pet.DoesNotExist:
            return JsonResponse({"error": "Pet not found."}, status=404)

        subscriptions = PushSubscription.objects.all()
        nearby_users = []

        for subscription in subscriptions:
            distance = calculate_distance(pet.latitude, pet.longitude, subscription.lat, subscription.lon)
            if distance <= subscription.distance:
                nearby_users.append(subscription)

        icon_url = f"{settings.DOMAIN_APP_URL}/static/logo192.png"  # adjust path
        badge_url = f"{settings.DOMAIN_APP_URL}/static/logo192.png"      # adjust path


        for subscription in nearby_users:
            # Check if the pet has an image URL in pet_image_1, otherwise use a default image
            image_url = pet.pet_image_1 or f"{settings.DOMAIN_APP_URL}/static/logo192.png"
            payload = {
                "title": f"Attention! A {pet.get_status_display()} pet is near you!",
                "body": f"A {pet.get_status_display()} {pet.get_species_display()} is near your location!",
                "url": f"{settings.DOMAIN_APP_URL}/pets/{pet.id}",
                "image": image_url,  # Add the image URL to the payload
                "icon": icon_url,
                "badge": badge_url,
                "actions": [
                    {"action": "view", "title": "View"},
                    {"action": "ignore", "title": "Ignore"}
                ]
            }
            send_push_notification(subscription, payload)

        return JsonResponse({"status": "Notifications sent to nearby users."})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pet_post_quota(request):
    user = request.user

    pet_limit = 5  # Global limit for all users
    current_count = Pet.objects.filter(author=user).count()
    remaining = max(pet_limit - current_count, 0)

    return Response({
        'limit': pet_limit,
        'used': current_count,
        'remaining': remaining
    })

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def pet_post_quota(request):
#     user = request.user

#     # Default limit for free users
#     pet_limit = 1

#     # Adjust based on subscription
#     if getattr(user, "is_subscribed", False):
#         if user.subscription_type == 'plus':
#             pet_limit = 3
#         elif user.subscription_type == 'premium':
#             pet_limit = 5

#     # Count how many pets the user has already posted
#     current_count = Pet.objects.filter(author=user).count()

#     remaining = max(pet_limit - current_count, 0)

#     return Response({
#         'limit': pet_limit,
#         'used': current_count,
#         'remaining': remaining
#     })

@api_view(['GET'])
@permission_classes([AllowAny])
def pet_view_stats(request, pet_id):
    """
    Get view statistics for a specific pet.
    Anyone can view these stats.
    """
    print(f"DEBUG: pet_view_stats called for pet_id: {pet_id}")
    try:
        pet = Pet.objects.get(id=pet_id)
        print(f"DEBUG: Found pet: {pet.id}")
        
        # Get all views for this pet
        all_views = PetView.objects.filter(pet=pet)
        all_shares = PetShare.objects.filter(pet=pet)
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
            'pet_id': pet_id,
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
        
    except Pet.DoesNotExist:
        print(f"DEBUG: Pet not found with ID: {pet_id}")
        return Response(
            {"error": "Pet not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def track_pet_share(request, pet_id):
    """
    Track when a pet is shared.
    """
    print(f"DEBUG: track_pet_share called for pet_id: {pet_id}")
    print(f"DEBUG: Request data: {request.data}")
    print(f"DEBUG: Request user: {request.user}")
    print(f"DEBUG: Request META: {dict(request.META)}")
    
    try:
        pet = Pet.objects.get(id=pet_id)
        print(f"DEBUG: Found pet: {pet.id}")
        
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
        
        # Check if this user/IP has already shared this pet today
        from django.utils import timezone
        from datetime import timedelta
        
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = today_start + timedelta(days=1)
        
        # Check for existing share today
        existing_share = None
        if request.user.is_authenticated:
            # For authenticated users, check by user
            existing_share = PetShare.objects.filter(
                pet=pet,
                user=request.user,
                method=share_method,
                created_at__gte=today_start,
                created_at__lt=today_end
            ).first()
        else:
            # For anonymous users, check by IP
            existing_share = PetShare.objects.filter(
                pet=pet,
                ip_address=ip,
                method=share_method,
                created_at__gte=today_start,
                created_at__lt=today_end
            ).first()
        
        # Only create a new share record if no share exists for today with this method
        if not existing_share:
            print(f"DEBUG: Creating PetShare record...")
            share_record = PetShare.objects.create(
                pet=pet,
                user=request.user if request.user.is_authenticated else None,
                ip_address=ip if not request.user.is_authenticated else None,
                method=share_method
            )
            print(f"DEBUG: Created share record with ID: {share_record.id}")
        else:
            print(f"DEBUG: Share already tracked today for this user/IP and method")
        
        return Response({
            'pet_id': pet_id,
            'method': share_method,
            'message': 'Share tracked successfully' if not existing_share else 'Share already tracked today'
        })
        
    except Pet.DoesNotExist:
        print(f"DEBUG: Pet not found with ID: {pet_id}")
        return Response(
            {"error": "Pet not found."}, 
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
def flag_pet(request, pet_id):
    """
    Flag a pet for inappropriate content.
    Requires authentication.
    """
    try:
        pet = Pet.objects.get(id=pet_id)
        
        # Get client IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Check if user has already flagged this pet
        existing_flag = PetReport.objects.filter(
            pet=pet,
            user=request.user
        ).first()
        
        if existing_flag:
            return Response(
                {"error": "You have already flagged this pet."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the flag
        flag = PetReport.objects.create(
            pet=pet,
            user=request.user,
            ip_address=ip
        )
        
        # Check if pet should be banned (5 or more unique flags)
        unique_flags_count = PetReport.objects.filter(pet=pet).count()
        
        if unique_flags_count >= 5:
            # Ban the pet
            pet.is_banned = True
            pet.save()
            
            return Response({
                'pet_id': pet_id,
                'message': 'Pet flagged successfully. Pet has been banned due to multiple flags.',
                'banned': True,
                'flag_count': unique_flags_count
            })
        else:
            return Response({
                'pet_id': pet_id,
                'message': 'Pet flagged successfully.',
                'banned': False,
                'flag_count': unique_flags_count
            })
        
    except Pet.DoesNotExist:
        return Response(
            {"error": "Pet not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Error flagging pet: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unflag_pet(request, pet_id):
    """
    Remove flag from a pet.
    Requires authentication.
    """
    try:
        pet = Pet.objects.get(id=pet_id)
        
        # Find and delete the user's flag
        flag = PetReport.objects.filter(
            pet=pet,
            user=request.user
        ).first()
        
        if not flag:
            return Response(
                {"error": "You have not flagged this pet."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        flag.delete()
        
        # Check if pet should be unbanned (less than 5 flags now)
        unique_flags_count = PetReport.objects.filter(pet=pet).count()
        
        if unique_flags_count < 5 and pet.is_banned:
            # Unban the pet
            pet.is_banned = False
            pet.save()
            
            return Response({
                'pet_id': pet_id,
                'message': 'Flag removed successfully. Pet has been unbanned.',
                'banned': False,
                'flag_count': unique_flags_count
            })
        else:
            return Response({
                'pet_id': pet_id,
                'message': 'Flag removed successfully.',
                'banned': unique_flags_count >= 5 and pet.is_banned,
                'flag_count': unique_flags_count
            })
        
    except Pet.DoesNotExist:
        return Response(
            {"error": "Pet not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": f"Error removing flag: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_pet_flag_status(request, pet_id):
    """
    Get the flag status for the current user and total flag count.
    """
    try:
        pet = Pet.objects.get(id=pet_id)
        
        # Check if current user has flagged this pet
        user_flagged = PetReport.objects.filter(
            pet=pet,
            user=request.user
        ).exists()
        
        # Get total flag count
        total_flags = PetReport.objects.filter(pet=pet).count()
        
        # Only consider banned if it has 5+ flags AND is banned
        is_banned_by_flags = total_flags >= 5 and pet.is_banned
        
        return Response({
            'pet_id': pet_id,
            'user_flagged': user_flagged,
            'total_flags': total_flags,
            'banned': is_banned_by_flags
        })
        
    except Pet.DoesNotExist:
        return Response(
            {"error": "Pet not found."}, 
            status=status.HTTP_404_NOT_FOUND
        )

class PosterDetailView(generics.RetrieveAPIView):
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    lookup_field = 'id'

class PetSightingPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'


class PetSightingView(APIView):
    """Handles creating pet sighting entry (POST), listing pet sightings (GET), and deleting a sighting (DELETE)"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, id):
        # List paginated pet sightings for a specific pet
        pet = get_object_or_404(Pet, id=id)
        sightings = PetSightingHistory.objects.filter(pet=pet)
        serializer = PetSightingHistorySerializer(sightings, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        # Create a new pet sighting entry
        pet = get_object_or_404(Pet, id=id)

            # ✅ Block new sightings if the pet report is closed
        if pet.is_closed:
            return Response(
                {"detail": "Ziņojums ir slēgts. Vairs nevar pievienot novērojumus."},
                status=status.HTTP_403_FORBIDDEN
            )

        status_value = request.data.get('status')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        notes = request.data.get('notes', '')
        reporter = request.user

        # Validate `status`
        try:
            status_value = int(status_value)
            if status_value not in dict(PetSightingHistory.STATUS_CHOICES):
                return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "Invalid status format"}, status=status.HTTP_400_BAD_REQUEST)

        # Handle image upload (if provided)
        image_url = None
        image = request.FILES.get('image')
        if image:
            uploaded_image = cloudinary.uploader.upload(image)
            image_url = uploaded_image.get("secure_url")


        # Validate latitude/longitude only if provided
        if latitude is not None and longitude is not None:
            try:
                latitude = Decimal(latitude)
                longitude = Decimal(longitude)
                if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
                    return Response({"error": "Latitude must be between -90 and 90 and longitude between -180 and 180."}, status=status.HTTP_400_BAD_REQUEST)
            except (InvalidOperation, ValueError):
                return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If no coordinates provided, require at least image or notes to be present
            if not image_url and not notes:
                return Response({"error": "Either coordinates, an image, or notes must be provided."}, status=status.HTTP_400_BAD_REQUEST)
        # Validate latitude/longitude
        # if latitude and longitude:
        #     try:
        #         latitude = Decimal(latitude)
        #         longitude = Decimal(longitude)
        #     except (InvalidOperation, ValueError):
        #         return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the pet sighting in the database
        sighting = PetSightingHistory.objects.create(
            pet=pet,
            status=status_value,
            latitude=latitude if latitude is not None else None,
            longitude=longitude if longitude is not None else None,
            # event_occurred_at=event_occurred_at,
            notes=notes,
            reporter=reporter,
            pet_image=image_url
        )


        # Return success response
        return Response({
            "id": sighting.id,
            "pet": sighting.pet.id,
            "status": sighting.get_status_display(),
            "latitude": sighting.latitude,
            "longitude": sighting.longitude,
            # "event_occurred_at": sighting.event_occurred_at,
            "notes": sighting.notes,
            "image": sighting.pet_image,
            "reporter": sighting.reporter.id,
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, id, sighting_id):
        """
        Delete a pet sighting entry.
        Only the user who reported the sighting (sighting.reporter) can delete it.
        """
        # Get the pet instance by its ID
        pet = get_object_or_404(Pet, id=id)
        
        # Get the pet sighting instance by its ID and ensure it belongs to the pet
        sighting = get_object_or_404(PetSightingHistory, id=sighting_id, pet=pet)

        # Ensure that only the user who reported the sighting can delete it
        if sighting.reporter != request.user:
            raise PermissionDenied("You are not authorized to delete this sighting.")

        # Perform the deletion
        sighting.delete()

        return Response({"message": "Pet sighting deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    

# class PetSightingView(APIView):
#     """
#     Handles creating pet sighting entry (POST), listing pet sightings (GET), and deleting a sighting (DELETE)
#     """
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request, id):
#         # List paginated pet sightings for a specific pet
#         pet = get_object_or_404(Pet, id=id)
#         sightings = PetSightingHistory.objects.filter(pet=pet).order_by('-created_at')

#         paginator = PetSightingPagination()
#         page = paginator.paginate_queryset(sightings, request)
#         serializer = PetSightingHistorySerializer(page, many=True)

#         return paginator.get_paginated_response(serializer.data)

#     def post(self, request, id):
#         # Create a new pet sighting entry
#         pet = get_object_or_404(Pet, id=id)

#         status_value = request.data.get('status')
#         latitude = request.data.get('latitude')
#         longitude = request.data.get('longitude')
#         notes = request.data.get('notes', '')
#         reporter = request.user

#         # Validate `status`
#         try:
#             status_value = int(status_value)
#             if status_value not in dict(PetSightingHistory.STATUS_CHOICES):
#                 return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)
#         except (ValueError, TypeError):
#             return Response({"error": "Invalid status format"}, status=status.HTTP_400_BAD_REQUEST)

#         # Handle image upload (if provided)
#         image_url = None
#         image = request.FILES.get('image')
#         if image:
#             uploaded_image = cloudinary.uploader.upload(image)
#             image_url = uploaded_image.get("secure_url")

#         # Validate latitude/longitude only if provided
#         if latitude is not None and longitude is not None:
#             try:
#                 latitude = Decimal(latitude)
#                 longitude = Decimal(longitude)
#                 if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
#                     return Response({"error": "Latitude must be between -90 and 90 and longitude between -180 and 180."}, status=status.HTTP_400_BAD_REQUEST)
#             except (InvalidOperation, ValueError):
#                 return Response({"error": "Invalid latitude or longitude format"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             # Require at least image or notes if no coordinates
#             if not image_url and not notes:
#                 return Response({"error": "Either coordinates, an image, or notes must be provided."}, status=status.HTTP_400_BAD_REQUEST)

#         # Save the pet sighting in the database
#         sighting = PetSightingHistory.objects.create(
#             pet=pet,
#             status=status_value,
#             latitude=latitude if latitude is not None else None,
#             longitude=longitude if longitude is not None else None,
#             notes=notes,
#             reporter=reporter,
#             pet_image=image_url
#         )

#         return Response({
#             "id": sighting.id,
#             "pet": sighting.pet.id,
#             "status": sighting.get_status_display(),
#             "latitude": sighting.latitude,
#             "longitude": sighting.longitude,
#             "notes": sighting.notes,
#             "image": sighting.pet_image,
#             "reporter": sighting.reporter.id,
#         }, status=status.HTTP_201_CREATED)


# @csrf_exempt
# def increment_poster_scan(request, poster_id):
#     if request.method == 'POST':
#         data = json.loads(request.body)

#         try:
#             poster = Poster.objects.get(id=poster_id)
#         except Poster.DoesNotExist:
#             return JsonResponse({"error": "Poster not found."}, status=404)

#         # If the poster has no location, store it from the scan
#         if not poster.has_location:
#             lat = data.get('latitude')
#             lon = data.get('longitude')
#             if lat is not None and lon is not None:
#                 poster.latitude = lat
#                 poster.longitude = lon
#                 poster.has_location = True

#         poster.scans += 1
#         poster.save()

#         return JsonResponse({
#             "status": "ok",
#             "scans": poster.scans,
#             "latitude": poster.latitude,
#             "longitude": poster.longitude
#         })    
# @csrf_exempt
# def set_poster_location(request, poster_id):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         poster = Poster.objects.get(id=poster_id)
#         if not poster.has_location:
#             poster.latitude = data['latitude']
#             poster.longitude = data['longitude']
#             poster.has_location = True
#             poster.save()
#         return JsonResponse({"status": "ok"})
    
# @csrf_exempt
# def increment_poster_scan(request, poster_id):
#     if request.method == 'POST':
#         poster = Poster.objects.get(id=poster_id)
#         poster.scans += 1
#         poster.save()
#         return JsonResponse({"status": "ok", "scans": poster.scans})





