from django.utils.html import format_html
from django.contrib import admin
from .models import Pet, Poster, PetSightingHistory, UserFavorites, PetView, PetShare, PetReport


@admin.register(Poster)
class PosterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pet',
        'name',
        'scans',
        'has_location',
        'latitude',
        'longitude',
        'created_at',
        'poster_preview'
    )
    list_filter = ('has_location', 'created_at', 'pet__species', 'pet__status')
    search_fields = ('id', 'name', 'pet__id')
    readonly_fields = ('created_at', 'poster_preview')

    def poster_preview(self, obj):
        """Display a thumbnail if poster has an image associated via the pet"""
        # Assuming poster itself doesn't store image, using pet_image_1 from related pet
        if obj.pet.pet_image_1:
            url = obj.pet.pet_image_1.url if hasattr(obj.pet.pet_image_1, 'url') else obj.pet.pet_image_1
            return format_html(
                '<img src="{}" style="max-width: 200px; height: auto;" />', url
            )
        return "No image"
    poster_preview.short_description = "Poster Preview"

@admin.register(Pet)
class ShelterAdmin(admin.ModelAdmin):
    list_display = (
        'pet_image_thumbnail',
        'id',
        'status',
        'species',
        'size',
        'gender',
        'age',
        'final_status',
        'is_public',
        'is_archived',
        'is_closed',
    )
    list_filter = ('species', 'gender', 'status', 'final_status', 'is_public', 'is_archived', 'is_closed')
    search_fields = (
        'id',
        'breed',
        'notes',
    )
    readonly_fields = ('pet_image_preview',)

    fieldsets = (
        ('Image Preview', {
            'fields': ('pet_image_preview',),
        }),
        ('Basic Info', {
            'fields': (
                'status',
                'species',
                'size',
                'gender',
                'age',
                'breed',
                'pattern',
                'primary_color',
                'secondary_color',
                'notes',
            )
        }),
        ('Location', {
            'fields': (
                'latitude',
                'longitude',
                'event_occurred_at',
            )
        }),
        ('Contact Info', {
            'fields': (
                'author',
                'phone_code',
                'contact_phone',
            )
        }),
        ('Images', {
            'fields': (
                'pet_image_1',
                'pet_image_2',
                'pet_image_3',
                'pet_image_4',
            )
        }),
        ('Status Flags', {
            'fields': (
                'final_status',
                'is_public',
                'is_archived',
                'is_closed',
                'is_banned',
            )
        }),
    )

    def pet_image_thumbnail(self, obj):
        if obj.pet_image_1:
            url = obj.pet_image_1.url if hasattr(obj.pet_image_1, 'url') else obj.pet_image_1
            return format_html(
                '<img src="{}" style="width: 50px; height: auto;" />', url
            )
        return "-"
    pet_image_thumbnail.short_description = "Image"

    def pet_image_preview(self, obj):
        if obj.pet_image_1:
            url = obj.pet_image_1.url if hasattr(obj.pet_image_1, 'url') else obj.pet_image_1
            return format_html(
                '<img src="{}" style="max-width: 300px; height: auto;" />', url
            )
        return "No image"
    pet_image_preview.short_description = "Image Preview"
    

@admin.register(PetView)
class PetViewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pet',
        'user',
        'ip_address',
        'created_at',
        'viewer_info'
    )
    list_filter = ('created_at', 'pet__species', 'pet__status')
    search_fields = ('pet__id', 'user__username', 'ip_address')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def viewer_info(self, obj):
        """Display who viewed the pet"""
        if obj.user:
            return f"User: {obj.user.username}"
        else:
            return f"Anonymous: {obj.ip_address}"
    viewer_info.short_description = "Viewer"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pet', 'user')

@admin.register(PetShare)
class PetShareAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pet',
        'user',
        'ip_address',
        'method',
        'created_at',
        'sharer_info'
    )
    list_filter = ('created_at', 'method', 'pet__species', 'pet__status')
    search_fields = ('pet__id', 'user__username', 'ip_address', 'method')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def sharer_info(self, obj):
        """Display who shared the pet"""
        if obj.user:
            return f"User: {obj.user.username}"
        else:
            return f"Anonymous: {obj.ip_address}"
    sharer_info.short_description = "Sharer"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pet', 'user')

@admin.register(PetReport)
class PetReportAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'pet',
        'user',
        'ip_address',
        'created_at',
        'reporter_info'
    )
    list_filter = ('created_at', 'pet__species', 'pet__status')
    search_fields = ('pet__id', 'user__username', 'ip_address')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def reporter_info(self, obj):
        """Display who flagged the pet"""
        if obj.user:
            return f"User: {obj.user.username}"
        else:
            return f"Anonymous: {obj.ip_address}"
    reporter_info.short_description = "Flagger"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('pet', 'user')

# ===========================================================
# GeoDjango improvements - quick notes
# ===========================================================

# Pet model now stores lat/lng as DecimalFields,
# which limits spatial queries and admin usability.

# ➤ IMPROVEMENT:
# Use GeoDjango's PointField:
# from django.contrib.gis.db import models as geomodels
# class Pet(models.Model):
#     location = geomodels.PointField(geography=True, null=True, blank=True)

# ➤ BENEFITS:
# - Query pets nearby (e.g. within 5 km)
# - Distance calculations
# - Spatial indexes via PostGIS
# - Map widget in Django admin:
#     class PetAdmin(GeoModelAdmin):
#         list_display = ('id', 'species', 'location')
# - Easy frontend maps (Leaflet, OpenLayers)

# ➤ MIGRATION:
# Combine lat/lng into:
#     pet.location = Point(pet.longitude, pet.latitude)
