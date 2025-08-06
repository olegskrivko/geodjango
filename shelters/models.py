from django.db import models
from django.contrib.gis.db import models as geomodels
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.conf import settings
from django.contrib.gis.geos import Point
from core.mixins import AddressMixin, ContactMixin


class AnimalType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Animal type")
    slug = models.SlugField(max_length=50, unique=True, blank=True, help_text="Stable, URL-safe code for this animal type (auto-generated)")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Animal type"
        verbose_name_plural = "Animal types"



class SocialMedia(models.Model):
    # Defining the available platforms as a set of choices
    PLATFORM_CHOICES = [
        (1, 'Facebook'),
        (2, 'Instagram'),
        (3, 'X'),
        (4, 'LinkedIn'),
        (5, 'YouTube'),
        (6, 'TikTok'),
    ]
    
    shelter = models.ForeignKey('Shelter', related_name='social_media', on_delete=models.CASCADE)
    platform = models.IntegerField(choices=PLATFORM_CHOICES, blank=False, null=False, verbose_name="Platform")
    profile_url = models.URLField()  # URL of the profile

    def __str__(self):
        return dict(self.PLATFORM_CHOICES).get(self.platform, "Unknown Platform")

    class Meta:
        unique_together = ('shelter', 'platform')

class Shelter( AddressMixin, ContactMixin, models.Model):
    
    SHELTER_CATEGORY_CHOICES = [
        (1, 'Municipal Shelter'),
        (2, 'Animal Rescue'),
        (3, 'Sanctuary'),
        (4, 'Private Shelter'),
    ]

    SHELTER_SIZE_CHOICES = [
        (1, 'Small (1-20 animals)'),
        (2, 'Medium (21-100 animals)'),
        (3, 'Large (100+ animals)'),
    ]

    animal_types = models.ManyToManyField(AnimalType, blank=True, related_name='shelters', verbose_name="Animal types")
    legal_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Legal entity Name")
    operating_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Operating Name")
    registration_number = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Registration Number")
    established_at = models.DateField(blank=True, null=True, verbose_name="Established Date")
    is_visible = models.BooleanField(default=True, verbose_name="Visible to public")
    is_offering_adoption = models.BooleanField(default=False, verbose_name="Offers adoption")
    is_accepting_volunteers = models.BooleanField(default=False, verbose_name="Accepts volunteers")
    is_accepting_donations = models.BooleanField(default=False, verbose_name="Accepts donations")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    size = models.IntegerField(choices=SHELTER_SIZE_CHOICES, blank=True, null=True, verbose_name="Size")
    category = models.IntegerField(choices=SHELTER_CATEGORY_CHOICES, blank=True, null=True, verbose_name="Category") 
    cover = CloudinaryField('image', blank=True, null=True, help_text="Cover image representing the shelter.")
    cover_prompt = models.TextField(blank=True, help_text="Optional prompt or description related to the shelter image.")
    cover_alt = models.CharField(max_length=255, blank=True, help_text="Alternative text for the shelter image.")
    cover_caption = models.CharField(max_length=255, blank=True, help_text="Caption or description for the shelter image.")
    cover_source = models.CharField(max_length=255, blank=True, help_text="Source or credit for the shelter image.")
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='shelters_created', help_text="User who created this shelter.")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='shelters_updated', help_text="User who last updated this shelter.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the shelter was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the shelter was last updated.")


    def __str__(self):
        return self.operating_name
    
    class Meta:
        verbose_name = "Shelter"
        verbose_name_plural = "Shelters"
        ordering = ['operating_name']