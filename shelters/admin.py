# from django.contrib import admin
# from .models import Shelter, SocialMedia, AnimalType
# from leaflet.admin import LeafletGeoAdmin
# from django.utils.html import format_html

# class SocialMediaInline(admin.TabularInline):
#     model = SocialMedia
#     extra = 1

# @admin.register(Shelter)
# class ShelterAdmin(LeafletGeoAdmin):
#     def cover_preview(self, obj):
#         if obj.cover:
#             return format_html('<img src="{}" width="200" style="object-fit:contain;"/>', obj.cover.url)
#         return "(No image)"

#     cover_preview.short_description = "Cover Preview"

#     list_display = (
#         'operating_name', 'country', 'city', 'street_address', 'postal_code', 'location',
#         'latitude', 'longitude', 'is_visible', 'is_offering_adoption',
#         'is_accepting_volunteers', 'is_accepting_donations', 'created_by', 'updated_by', 'created_at', 'updated_at',
#     )

#     list_filter = (
#         'country', 'state_or_province', 'city', 'is_visible', 'is_offering_adoption',
#         'is_accepting_volunteers', 'is_accepting_donations', 'category', 'size'
#     )

#     search_fields = (
#         'operating_name', 'city', 'street_address', 'postal_code', 'email'
#     )

#     filter_horizontal = ('animal_types',)
#     inlines = [SocialMediaInline]

#     readonly_fields = ('full_address','created_by', 'updated_by', 'created_at', 'updated_at', 'cover_preview',)

#     fieldsets = (
#         ('General Info', {
#             'fields': (
#                 'operating_name', 'legal_name', 'registration_number', 'established_at', 
#                 'description', 'website_url', 
#                 'cover', 'cover_preview', 'cover_prompt', 'cover_alt', 'cover_caption', 'cover_source',
#                 'animal_types', 'category', 'size',
#                 'country', 'state_or_province', 'city',
#                 'street_address', 'street_address2', 'postal_code',
#                 'full_address', 'location', 'latitude', 'longitude'
#             )
#         }),

#         ('Contact & Access', {
#             'fields': (
#                 'country_code', 'national_number', 'email',
#                 'is_visible', 'is_offering_adoption',
#                 'is_accepting_volunteers', 'is_accepting_donations', 
#             ),
#         }),
#           ('Audit Trail', {
#             'fields': (
#                 'created_by', 'updated_by', 'created_at', 'updated_at',
#             )
#         })
#     )

# @admin.register(AnimalType)
# class AnimalTypeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     search_fields = ('name', 'slug')
#     readonly_fields = ('slug',)  

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Shelter, AnimalType
from core.models import SocialMedia  # Now in core
from leaflet.admin import LeafletGeoAdmin
from django.utils.html import format_html


class SocialMediaInline(GenericTabularInline):
    model = SocialMedia
    extra = 1


@admin.register(Shelter)
class ShelterAdmin(LeafletGeoAdmin):
    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" width="200" style="object-fit:contain;"/>', obj.cover.url)
        return "(No image)"
    cover_preview.short_description = "Cover Preview"

    list_display = (
        'operating_name', 'country', 'city', 'street_address', 'postal_code', 'location',
        'latitude', 'longitude', 'is_visible', 'is_offering_adoption',
        'is_accepting_volunteers', 'is_accepting_donations', 'created_by', 'updated_by', 'created_at', 'updated_at',
    )
    list_filter = (
        'country', 'state_or_province', 'city', 'is_visible', 'is_offering_adoption',
        'is_accepting_volunteers', 'is_accepting_donations', 'category', 'size'
    )
    search_fields = (
        'operating_name', 'city', 'street_address', 'postal_code', 'email'
    )
    filter_horizontal = ('animal_types',)
    inlines = [SocialMediaInline]
    readonly_fields = ('full_address', 'created_by', 'updated_by', 'created_at', 'updated_at', 'cover_preview',)

    fieldsets = (
        ('General Info', {
            'fields': (
                'operating_name', 'legal_name', 'registration_number', 'established_at',
                'description', 'website_url',
                'cover', 'cover_preview', 'cover_prompt', 'cover_alt', 'cover_caption', 'cover_source',
                'animal_types', 'category', 'size',
                'country', 'state_or_province', 'city',
                'street_address', 'street_address2', 'postal_code',
                'full_address', 'location', 'latitude', 'longitude'
            )
        }),
        ('Contact & Access', {
            'fields': (
                'country_code', 'national_number', 'email',
                'is_visible', 'is_offering_adoption',
                'is_accepting_volunteers', 'is_accepting_donations',
            ),
        }),
        ('Audit Trail', {
            'fields': (
                'created_by', 'updated_by', 'created_at', 'updated_at',
            )
        })
    )


@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    readonly_fields = ('slug',)
