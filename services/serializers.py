# services/serializers.py
from rest_framework import serializers
from .models import Service,  Review,  Location , WorkingHour, SocialMedia
import logging
import json
from django.contrib.gis.geos import Point
logger = logging.getLogger(__name__)


class SocialMediaSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='get_platform_display', read_only=True)

    class Meta:
        model = SocialMedia
        fields = ['platform', 'profile_url']

class WorkingHourSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display')

    class Meta:
        model = WorkingHour
        fields = '__all__' 

class LocationSerializer(serializers.ModelSerializer):
    working_hours = WorkingHourSerializer(many=True, read_only=True)
    full_address = serializers.ReadOnlyField()
    distance_km = serializers.SerializerMethodField()




    def get_distance_km(self, obj):
        # Distance annotated in queryset as meters (default unit)
        distance = getattr(obj, 'distance', None)
        if distance is not None:
            # Convert meters to kilometers and round
            return round(distance.m / 1000, 2)
        return None

    # def get_distance_km(self, obj):
    #     user_point = self.context.get('user_point')
    #     if user_point and obj.location:
    #         distance_m = obj.location.distance(user_point)  # distance in degrees
    #         # Convert degrees to meters (approx)
    #         # For geographic (lon/lat), use Distance function to get meters accurately:
    #         # Better: annotate location queryset with Distance() in meters, but here quick calc:
    #         # Instead, use geodjango Distance function to get meters (if obj.location is geographic Point)
            
    #         # Actually better approach:
    #         from django.contrib.gis.measure import Distance as D
    #         # Calculate distance in meters using geodjango:
    #         dist = obj.location.distance(user_point)
    #         # dist is in degrees, so convert by:
    #         from django.contrib.gis.geos import GEOSGeometry
    #         # Instead let's annotate in queryset (better), or approximate meters as below:
    #         # Approximate conversion: 1 degree ~ 111 km
    #         distance_km = dist * 111  # very rough
    #         return round(distance_km, 2)
    #     return None

    
    class Meta:
        model = Location
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    full_phone_number = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    social_media = SocialMediaSerializer(many=True, read_only=True)
    cover_url = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')  # Optional: Display username
    category_display = serializers.CharField(source='get_category_display', read_only=True)  # 👈 Add this
    provider_display = serializers.CharField(source='get_provider_display', read_only=True)
    price_type_display = serializers.CharField(source='get_price_type_display', read_only=True)
    
    service_image_1 = serializers.URLField(required=False, allow_blank=True)
    service_image_2 = serializers.URLField(required=False, allow_blank=True)
    service_image_3 = serializers.URLField(required=False, allow_blank=True)
    service_image_4 = serializers.URLField(required=False, allow_blank=True)

    locations = LocationSerializer(many=True, read_only=True) 
    # here i need to show location from current locations, which is the nearesest to the user.
    #min_distance_km 


    min_distance_km = serializers.SerializerMethodField()

    def get_min_distance_km(self, obj):
    # Use getattr with default None to avoid AttributeError
        distance = getattr(obj, 'min_distance_km', None)
        return round(distance, 2) if distance is not None else None

    # def get_min_distance_km(self, obj):
    #     return round(obj.min_distance_km, 2) if obj.min_distance_km is not None else None

    # def get_min_distance_km(self, obj):
    #     locations = obj.locations.all()
    #     if not locations:
    #         return None

    #     distances = [
    #         loc.distance.km for loc in locations
    #         if hasattr(loc, 'distance') and loc.distance is not None
    #     ]
    #     return round(min(distances), 2) if distances else None




    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()


    def get_cover_url(self, obj):
        if obj.cover:
            # CloudinaryField has .url property
            return obj.cover.url
        return None

    def get_rating(self, obj):
        return round(obj.average_rating(), 1)  # Use the method defined in the model

    def get_review_count(self, obj):
        return obj.review_count()  # Call the review_count() method from the Service model

    def validate(self, data):
        request = self.context.get('request')
        print("validated data in serializer:", data)

        if request and request.method == 'POST':
            # We must check locations from the raw request because DRF won't parse nested JSON in multipart
            raw_locations = request.data.get('locations')
            if isinstance(raw_locations, list):
                raw_locations = raw_locations[0]

            try:
                parsed_locations = json.loads(raw_locations)
            except (TypeError, json.JSONDecodeError):
                parsed_locations = []

            if not parsed_locations:
                raise serializers.ValidationError({
                    "locations": "At least one location is required when creating a service."
                })

        return data

    def create(self, validated_data):
        locations_data = validated_data.pop('locations', [])
        social_media_data = validated_data.pop('social_media', [])

        logger.debug("Creating service with validated_data: %s", validated_data)
        logger.debug("Locations data: %s", locations_data)
        logger.debug("Social media data: %s", social_media_data)

        try:
            service = Service.objects.create(**validated_data)
        except Exception as e:
            logger.exception("Error creating Service instance")
            raise serializers.ValidationError({"service_creation": str(e)})

        for loc_data in locations_data:
            try:
                Location.objects.create(service=service, **loc_data)
            except Exception as e:
                logger.exception("Error creating Location with data: %s", loc_data)
                raise serializers.ValidationError({"location_creation": str(e)})

        if social_media_data:
            try:
                service.social_media.set(social_media_data)
            except Exception as e:
                logger.exception("Error setting social media")
                raise serializers.ValidationError({"social_media": str(e)})

        return service

    def update(self, instance, validated_data):
        locations_data = validated_data.pop('locations', None)
        social_media_data = validated_data.pop('social_media', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if social_media_data is not None:
            instance.social_media.set(social_media_data)

        if locations_data is not None:
            # Remove old locations
            instance.locations.all().delete()
            for loc_data in locations_data:
                Location.objects.create(service=instance, **loc_data)

        return instance

    class Meta:
        model = Service
        fields = '__all__' 

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.CharField(source='user.avatar', read_only=True)

    def validate_rating(self, value):
        if value is None:
            raise serializers.ValidationError("Rating is required.")
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
 
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at', 'user_name', 'user_avatar', 'user', 'service']
        read_only_fields = ['id', 'created_at', 'user', 'service']


