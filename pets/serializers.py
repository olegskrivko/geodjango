# pets/serializers.py
from rest_framework import serializers
from .models import Pet, PetSightingHistory
from django.contrib.auth import get_user_model
from .models import Poster
# from .models import Animal
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar']

class PetSightingHistorySerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')
    status = serializers.IntegerField()  # This ensures you return the raw integer value, not the display string
    reporter = UserSerializer(read_only=True)  # Serialize the User field
    pet_image = serializers.CharField(required=False, allow_blank=True)  # ✅ Accepts empty values
    pet = serializers.PrimaryKeyRelatedField(queryset=Pet.objects.all())  # ✅ Ensure `pet` exists
    #event_occurred_at = serializers.DateTimeField(required=False, allow_null=True)  # ✅ Ensure it's an aware datetime
    class Meta:
        model = PetSightingHistory
        fields = '__all__' 


    # def get_image_url(self, obj):
    #     print("self",self)
    #     """ ✅ Return Cloudinary Image URL for sightings """
    #     return obj.image if obj.image else None

    # def validate(self, data):
    #     latitude = data.get('latitude')
    #     longitude = data.get('longitude')
    #     pet_image = data.get('pet_image')
    #     notes = data.get('notes')

    #     # If latitude or longitude is missing, require pet_image or notes
    #     if latitude is None or longitude is None:
    #         if not pet_image and not notes:
    #             raise serializers.ValidationError(
    #                 "Either coordinates, an image, or notes must be provided."
    #             )
    #     else:
    #         # Validate latitude and longitude ranges
    #         try:
    #             lat = float(latitude)
    #             lon = float(longitude)
    #         except (TypeError, ValueError):
    #             raise serializers.ValidationError("Latitude and longitude must be valid numbers.")

    #         if not (-90 <= lat <= 90):
    #             raise serializers.ValidationError("Latitude must be between -90 and 90 degrees.")
    #         if not (-180 <= lon <= 180):
    #             raise serializers.ValidationError("Longitude must be between -180 and 180 degrees.")

    #     return data

    # def validate(self, data):
    #     # Check if latitude and longitude are provided and are valid
    #     """Ensure latitude and longitude are valid."""
    #     latitude = data.get('latitude')
    #     longitude = data.get('longitude')

    #     if not latitude or not longitude:
    #         raise serializers.ValidationError("Latitude and longitude must be provided.")
        
    #     try:
    #         latitude = float(latitude)
    #         longitude = float(longitude)
    #     except ValueError:
    #         raise serializers.ValidationError("Latitude and longitude must be valid numbers.")

    #     # Optionally, check for valid ranges
    #     if not (-90 <= latitude <= 90):
    #         raise serializers.ValidationError("Latitude must be between -90 and 90 degrees.")
    #     if not (-180 <= longitude <= 180):
    #         raise serializers.ValidationError("Longitude must be between -180 and 180 degrees.")
        
    #     return data


class PetSerializer(serializers.ModelSerializer):

    # This will return the human-readable values
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    species_display = serializers.CharField(source='get_species_display', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    age_display = serializers.CharField(source='get_age_display', read_only=True)
    pattern_display = serializers.CharField(source='get_pattern_display', read_only=True)
    primary_color_display = serializers.CharField(source='get_primary_color_display', read_only=True)
    secondary_color_display = serializers.CharField(source='get_secondary_color_display', read_only=True)
    contact_phone_display = serializers.CharField(source='get_contact_phone_display', read_only=True)
    final_status_display = serializers.CharField(source='get_final_status_display', read_only=True)
    
    
    pet_image_1 = serializers.URLField(required=False, allow_blank=True)
    pet_image_2 = serializers.URLField(required=False, allow_blank=True)
    pet_image_3 = serializers.URLField(required=False, allow_blank=True)
    pet_image_4 = serializers.URLField(required=False, allow_blank=True)

    author = UserSerializer(read_only=True)  # Add the UserSerializer here
    
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=True)

    
    is_closed = serializers.BooleanField(required=False)
    distance_from_riga_km = serializers.ReadOnlyField()

    distance_km = serializers.SerializerMethodField()
    # def get_distance(self, obj):
    #     if hasattr(obj, 'distance') and obj.distance is not None:
    #         return round(obj.distance.km, 2)  # You can use .m, .mi, .km, etc.
    #     return None
    
    def get_distance_km(self, obj):
        if hasattr(obj, 'distance') and obj.distance:
            return round(obj.distance.km, 2)
        return None
    
    class Meta:
        model = Pet
        fields = '__all__'  # Include all fields from the model

    
        

    def create(self, validated_data):
        print("🔥 PetSerializer.create() hit!")  # Debugging Line
        pet = Pet.objects.create(**validated_data)
        print(f"✅ Pet {pet.id} saved successfully!") # Debugging Line
        return pet


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = '__all__'



