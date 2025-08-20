

# core/models.py (or wherever you keep shared models)
from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
import cloudinary.api
from .choices import COUNTRY_CHOICES
from .mixins import ContactMixin
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CoverImageModel(models.Model):
    cover = CloudinaryField('image', blank=True, null=True, help_text="Cover image.")
    cover_width = models.PositiveIntegerField(null=True, blank=True)
    cover_height = models.PositiveIntegerField(null=True, blank=True)
    cover_format = models.CharField(max_length=50, blank=True)
    cover_size = models.PositiveIntegerField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_cover = self.cover

    def save(self, *args, **kwargs):
        if not self.cover:
            self.cover_width = None
            self.cover_height = None
            self.cover_format = ''
            self.cover_size = None
        else:
            if self.cover != self._original_cover:
                try:
                    public_id = self.cover.public_id
                    resource = cloudinary.api.resource(public_id)
                    self.cover_width = resource.get('width')
                    self.cover_height = resource.get('height')
                    self.cover_format = resource.get('format')
                    self.cover_size = resource.get('bytes')
                except Exception as e:
                    # Consider logging here instead of print
                    print(f"Error fetching Cloudinary metadata: {e}")
        super().save(*args, **kwargs)
        self._original_cover = self.cover

    class Meta:
        abstract = True
        
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class AuditableModel(TimeStampedModel):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True

class Animal(models.Model):
    STATUS_CHOICES = [
        (1, 'Available'),
        (2, 'Adopted'),
        (3, 'Fostered'),
    ]

    SPECIES_CHOICES = [
        (1, 'Dog'),
        (2, 'Cat'),
        (3, 'Bird'),
        (4, 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    species = models.IntegerField(choices=SPECIES_CHOICES)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    image = CloudinaryField('image', blank=True, null=True)
    #image = models.URLField(blank=True, null=True)  # Store URL string only

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question
        
# class FAQ(models.Model):
#     question = models.CharField(max_length=255)
#     answer = models.TextField()
#     is_active = models.BooleanField(default=True)
#     order = models.PositiveIntegerField(default=0)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return self.question
    
class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        (1, 'Facebook'),
        (2, 'Instagram'),
        (3, 'X'),
        (4, 'LinkedIn'),
        (5, 'YouTube'),
        (6, 'TikTok'),
    ]

    # Generic relation fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    platform = models.IntegerField(choices=PLATFORM_CHOICES)
    profile_url = models.URLField()

    def __str__(self):
        return f"{dict(self.PLATFORM_CHOICES).get(self.platform, 'Unknown')} - {self.profile_url}"

    class Meta:
        verbose_name = "Social Media"
        verbose_name_plural = "Social Media Links"
        # Ensure that for each related object (e.g., a shelter), there can be only one entry per social media platform
        unique_together = ('content_type', 'object_id', 'platform')
