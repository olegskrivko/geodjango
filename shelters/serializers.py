from rest_framework import serializers
from .models import Shelter, SocialMedia, AnimalType
from django.contrib.gis.geos import Point


class AnimalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalType
        fields = ['id', 'name', 'slug']

class SocialMediaSerializer(serializers.ModelSerializer):
    platform = serializers.CharField(source='get_platform_display', read_only=True)
    class Meta:
        model = SocialMedia
        fields = ['platform', 'profile_url']

class ShelterSerializer(serializers.ModelSerializer):
    full_phone_number = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    distance_from_riga_km = serializers.ReadOnlyField()
    animal_types = AnimalTypeSerializer(many=True, read_only=True)
    social_media = SocialMediaSerializer(many=True, read_only=True)
    cover_url = serializers.SerializerMethodField()

    distance_km = serializers.SerializerMethodField()
    
    
    def get_distance_km(self, obj):
        if hasattr(obj, 'distance') and obj.distance:
            return round(obj.distance.km, 2)
        return None
    
    def validate(self, data):
        lat = data.get('latitude')
        lng = data.get('longitude')
        if (lat is None) != (lng is None):  # only one is provided
            raise serializers.ValidationError("Both latitude and longitude must be provided together.")
        if lat is not None and lng is not None:
            data['location'] = Point(float(lng), float(lat))
        return data

    class Meta:
        model = Shelter
        fields =  '__all__'

    def get_cover_url(self, obj):
        if obj.cover:
            # CloudinaryField has .url property
            return obj.cover.url
        return None