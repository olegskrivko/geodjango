# services/serializers.py
from rest_framework import serializers
from .models import Service,  Review,  Location , WorkingHour, SocialMedia,  ServiceCategory
import logging
import json
from django.contrib.gis.geos import Point
logger = logging.getLogger(__name__)


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'slug']

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

    class Meta:
        model = Location
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    full_phone_number = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    social_media = SocialMediaSerializer(many=True, read_only=True)
    cover_url = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source='user.username')  # Optional: Display username
    # category_display = serializers.CharField(source='get_category_display', read_only=True)
    service_categories = ServiceCategorySerializer(many=True, read_only=True)
    provider_display = serializers.CharField(source='get_provider_display', read_only=True)
    price_type_display = serializers.CharField(source='get_price_type_display', read_only=True)
    
    service_image_1 = serializers.URLField(required=False, allow_blank=True)
    service_image_2 = serializers.URLField(required=False, allow_blank=True)
    service_image_3 = serializers.URLField(required=False, allow_blank=True)
    service_image_4 = serializers.URLField(required=False, allow_blank=True)

    locations = LocationSerializer(many=True, read_only=True) 
    min_distance_km = serializers.SerializerMethodField()

    def get_min_distance_km(self, obj):
        # Use getattr with default None to avoid AttributeError
        distance = getattr(obj, 'min_distance_km', None)
        return round(distance, 2) if distance is not None else None

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
            print("🔍 Raw locations from request:", raw_locations)
            print("🔍 Request data keys:", list(request.data.keys()))
            
            if isinstance(raw_locations, list):
                raw_locations = raw_locations[0]

            try:
                parsed_locations = json.loads(raw_locations)
                print("🔍 Parsed locations:", parsed_locations)
            except (TypeError, json.JSONDecodeError) as e:
                print("❌ Error parsing locations JSON:", e)
                parsed_locations = []

            if not parsed_locations:
                raise serializers.ValidationError({
                    "locations": "At least one location is required when creating a service."
                })

            # Store locations in context for later use in create method
            self.context['locations_data'] = parsed_locations
            print("🔍 Locations stored in context:", self.context['locations_data'])

            # Handle service categories from raw request
            raw_service_categories = request.data.get('service_categories')
            if raw_service_categories:
                try:
                    if isinstance(raw_service_categories, list):
                        parsed_categories = raw_service_categories[0]
                    else:
                        parsed_categories = raw_service_categories
                    
                    service_categories = json.loads(parsed_categories)
                    print("🔍 Parsed service categories:", service_categories)
                    
                    # Validate max 3 categories
                    if len(service_categories) > 3:
                        raise serializers.ValidationError({
                            "service_categories": "You can select up to 3 service categories."
                        })
                    
                    # Store categories in context for later use in create method
                    self.context['service_categories_data'] = service_categories
                    print("🔍 Service categories stored in context:", self.context['service_categories_data'])
                    
                except (TypeError, json.JSONDecodeError) as e:
                    print("❌ Error parsing service categories JSON:", e)
                    raise serializers.ValidationError({
                        "service_categories": "Invalid format for service categories."
                    })

        return data

    def create(self, validated_data):
        # Get locations from context (set during validation)
        locations_data = self.context.get('locations_data', [])
        social_media_data = validated_data.pop('social_media', [])
        service_categories_data = self.context.get('service_categories_data', [])
        request = self.context.get('request')

        logger.debug("Creating service with validated_data: %s", validated_data)
        logger.debug("Locations data: %s", locations_data)
        logger.debug("Social media data: %s", social_media_data)
        logger.debug("Service categories data: %s", service_categories_data)
        
        print("🚀 CREATE METHOD - Starting service creation")
        print("🚀 Validated data:", validated_data)
        print("🚀 Locations data from context:", locations_data)
        print("🚀 Service categories data from context:", service_categories_data)
        print("🚀 Number of locations:", len(locations_data))
        print("🚀 Number of service categories:", len(service_categories_data))

        # Handle image uploads
        print("🚀 Handling image uploads...")
        uploaded_images = {}
        uploaded_images_list = []
        
        for i in range(1, 5):
            image_field = f"service_image_{i}_media"
            image = request.FILES.get(image_field) if request else None
            if image:
                print(f"🚀 Uploading image {i}: {image.name}")
                try:
                    import cloudinary.uploader
                    uploaded_image = cloudinary.uploader.upload(image)
                    uploaded_images_list.append(uploaded_image.get("secure_url"))
                    print(f"✅ Image {i} uploaded successfully: {uploaded_image.get('secure_url')}")
                except Exception as e:
                    print(f"❌ Error uploading image {i}: {e}")
                    raise serializers.ValidationError({"image_upload": f"Failed to upload image {i}: {str(e)}"})

        if not uploaded_images_list:
            raise serializers.ValidationError({"error": "At least one image must be uploaded."})

        # Map images to service fields
        for idx, url in enumerate(uploaded_images_list):
            uploaded_images[f"service_image_{idx+1}"] = url
        for idx in range(len(uploaded_images_list) + 1, 5):
            uploaded_images[f"service_image_{idx}"] = None

        print(f"🚀 Image URLs mapped: {uploaded_images}")

        try:
            print("🚀 Creating Service instance...")
            # Add image URLs to validated data
            validated_data.update(uploaded_images)
            service = Service.objects.create(**validated_data)
            print("✅ Service created successfully with ID:", service.id)
            
            # Set service categories
            if service_categories_data:
                try:
                    print("🚀 Setting service categories:", service_categories_data)
                    # Get ServiceCategory instances by slug
                    from .models import ServiceCategory
                    categories = ServiceCategory.objects.filter(slug__in=service_categories_data)
                    if categories.exists():
                        service.service_categories.set(categories)
                        print(f"✅ Set {categories.count()} service categories on service")
                    else:
                        print("⚠️ No ServiceCategory instances found for slugs:", service_categories_data)
                except Exception as e:
                    print(f"❌ Error setting service categories: {e}")
                    logger.exception("Error setting service categories")
            
        except Exception as e:
            print("❌ Error creating Service instance:", str(e))
            logger.exception("Error creating Service instance")
            raise serializers.ValidationError({"service_creation": str(e)})

        # Create locations with proper field mapping
        print("🚀 Starting location creation...")
        for i, loc_data in enumerate(locations_data):
            try:
                print(f"🚀 Creating location {i+1}:", loc_data)
                
                # Map frontend fields to backend model fields (now using correct names)
                location_fields = {
                    'service': service,
                    'location_title': loc_data.get('location_title', ''),
                    'location_description': loc_data.get('location_description', ''),
                    'street_address': loc_data.get('street_address', ''),
                    'city': loc_data.get('city', ''),
                    'state_or_province': loc_data.get('state_or_province', ''),
                    'postal_code': loc_data.get('postal_code', ''),
                    'latitude': loc_data.get('latitude'),
                    'longitude': loc_data.get('longitude'),
                }
                
                print(f"🚀 Location fields mapped:", location_fields)
                
                # Create Point geometry if coordinates are provided
                if loc_data.get('latitude') and loc_data.get('longitude'):
                    try:
                        lat = float(loc_data['latitude'])
                        lng = float(loc_data['longitude'])
                        location_fields['location'] = Point(lng, lat, srid=4326)
                        print(f"🚀 Point geometry created: ({lng}, {lat})")
                    except (ValueError, TypeError) as e:
                        print(f"❌ Error creating Point geometry: {e}")
                        logger.warning(f"Invalid coordinates: lat={loc_data.get('latitude')}, lng={loc_data.get('longitude')}")
                
                print(f"🚀 Creating Location object with fields:", location_fields)
                location = Location.objects.create(**location_fields)
                print(f"✅ Location {i+1} created successfully with ID:", location.id)
                
                # Create default working hours (Mon-Fri 9:00-17:00)
                print(f"🚀 Creating working hours for location {i+1}...")
                from datetime import time
                default_hours = [(i, time(9, 0), time(17, 0)) for i in range(5)]
                for day, start, end in default_hours:
                    working_hour = WorkingHour.objects.create(
                        location=location,
                        day=day,
                        from_hour=start,
                        to_hour=end
                    )
                    print(f"✅ Working hour created for day {day}: {start}-{end}")
                    
            except Exception as e:
                print(f"❌ Error creating Location {i+1}:", str(e))
                logger.exception("Error creating Location with data: %s", loc_data)
                raise serializers.ValidationError({"location_creation": str(e)})

        if social_media_data:
            try:
                service.social_media.set(social_media_data)
            except Exception as e:
                logger.exception("Error setting social media")
                raise serializers.ValidationError({"social_media": str(e)})

        print("✅ All locations and working hours created successfully!")
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


