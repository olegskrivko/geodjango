# Create your models here.
# services/models.py
from django.db import models
from django.contrib.auth import get_user_model
# from core.models import SocialMedia
from django.conf import settings
from django.db.models import Avg
#from django.contrib.gis.db import models as geomodels
from core.mixins import AddressMixin, ContactMixin
from cloudinary.models import CloudinaryField
from django.db.models import OuterRef, Subquery
User = get_user_model()



class SocialMedia(models.Model):
    # Defining the available platforms as a set of choices
    PLATFORM_CHOICES = [
        (1, 'Facebook'),
        (2, 'Instagram'),
        (3, 'X'),
        (4, 'LinkedIn'),
        (5, 'YouTube'),
        (6, 'TikTok'),
        (7, 'Pinterest'),
        (8, 'Snapchat'),
    ]
    
    service = models.ForeignKey('Service', related_name='social_media', on_delete=models.CASCADE)
    platform = models.IntegerField(choices=PLATFORM_CHOICES, blank=False, null=False, verbose_name="Platform")
    profile_url = models.URLField()  # URL of the profile
    is_official = models.BooleanField(default=False)  # Whether it's an official profile (e.g., government, embassy)
    is_verified = models.BooleanField(default=False)  # Whether the profile is verified (default to False)

    def __str__(self):
        return dict(self.PLATFORM_CHOICES).get(self.platform, "Unknown Platform")

    class Meta:
        unique_together = ('service', 'platform')
    
class Service(ContactMixin, models.Model):
    SERVICE_CATEGORIES = [
        (1, 'Sitting'),
        (2, 'Walking'), 
        (3, 'Grooming'),  
        (4, 'Training'), 
        (5, 'Boarding'), 
        (6, 'Veterinary'), 
        (7, 'Photography'),  
        (8, 'Rescue'),  
        (9, 'Supplies'), 
        (10, 'Art'),  
        (11, 'Burial'),  
        (12, 'Transport'),   
        (13, 'Breeders'), 
        (14, 'Insurance'), 
        (15, 'Miscellaneous'),  
    ]
    PROVIDER_TYPES = [
        (1, 'Individual'),
        (2, 'Company'),
    ]
    PRICE_TYPE_CHOICES = [
        (1, 'Per Hour'),
        (2, 'Per Unit'),
        (3, 'Per Day'),
        (4, 'By Agreement'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    
    legal_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Legal entity Name")
    operating_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Operating Name")
    registration_number = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Registration Number")
    established_at = models.DateField(blank=True, null=True, verbose_name="Established Date")
    description = models.TextField()
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_type = models.IntegerField(choices=PRICE_TYPE_CHOICES, default=1)    
    category = models.IntegerField(choices=SERVICE_CATEGORIES)
    provider = models.IntegerField(choices=PROVIDER_TYPES)

    cover = CloudinaryField('image', blank=True, null=True, help_text="Cover image representing the service.")
    cover_prompt = models.TextField(blank=True, help_text="Optional prompt or description related to the service image.")
    cover_alt = models.CharField(max_length=255, blank=True, help_text="Alternative text for the service image.")
    cover_caption = models.CharField(max_length=255, blank=True, help_text="Caption or description for the service image.")
    cover_source = models.CharField(max_length=255, blank=True, help_text="Source or credit for the service image.")
    
    cover_width = models.PositiveIntegerField(null=True, blank=True, help_text="Width of the service image in pixels.")
    cover_height = models.PositiveIntegerField(null=True, blank=True, help_text="Height of the service image in pixels.")
    cover_format = models.CharField(max_length=50, blank=True, help_text="Image format of the service (e.g., jpg, png).")
    cover_size = models.PositiveIntegerField(null=True, blank=True, help_text="File size of the service image in bytes.")

    is_active = models.BooleanField(default=True) 
    is_available = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False, verbose_name="Is Banned?")
    is_online = models.BooleanField(default=False)
    
    service_image_1 = models.URLField(max_length=255, null=False, blank=False, verbose_name="Servisa 1. attēls")
    service_image_2 = models.URLField(max_length=255, null=True, blank=True, verbose_name="Servisa 2. attēls")
    service_image_3 = models.URLField(max_length=255, null=True, blank=True, verbose_name="Servisa 3. attēls")
    service_image_4 = models.URLField(max_length=255, null=True, blank=True, verbose_name="Servisa 4. attēls")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='services_created', help_text="User who created this service.")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='services_updated', help_text="User who last updated this service.")
    
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the service was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the service was last updated.")
    

    def average_rating(self):
        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0

    def review_count(self):
        return self.reviews.count()
    
    def __str__(self):
        return self.operating_name
    
class Review(models.Model):
    service = models.ForeignKey(Service, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # 0.0 to 5.0
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        unique_together = ('service', 'user')
    
class Location(AddressMixin, models.Model):
    service = models.ForeignKey(Service, related_name='locations', on_delete=models.CASCADE)
    location_title = models.CharField(max_length=100)
    location_description = models.TextField()
    
    def __str__(self):
        return f'{self.service.operating_name} location'
    


class WorkingHour(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Monday'), 
        (1, 'Tuesday'), 
        (2, 'Wednesday'), 
        (3, 'Thursday'), 
        (4, 'Friday'), 
        (5, 'Saturday'), 
        (6, 'Sunday'), 
    ]

    location = models.ForeignKey(Location, related_name='working_hours', on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    class Meta:
        unique_together = ('location', 'day')
        ordering = ['day']

    def __str__(self):
        return f'{self.location.city} - {self.get_day_display()}: {self.from_hour}–{self.to_hour}'

class UserServiceFavorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_favorites")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'service'], name='unique_user_service')]

    def __str__(self):
        return f"{self.user.username} - {self.service.id}"



class ServiceView(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="User who viewed",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service View"
        verbose_name_plural = "Service Views"
        ordering = ['-created_at']

    def __str__(self):
        return f"View of Service {self.service.id} by {self.user or self.ip_address}"

class ServiceShare(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="User who shared",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    method = models.CharField(max_length=50, default='unknown')  # facebook, twitter, copy_link, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Share"
        verbose_name_plural = "Service Shares"
        ordering = ['-created_at']

    def __str__(self):
        return f"Share of Service {self.service.id} by {self.user or self.ip_address} via {self.method}"

class ServiceReport(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="User who reported",
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Report"
        verbose_name_plural = "Service Reports"
        ordering = ['-created_at']
        # Ensure one report per user/IP per service
        constraints = [
            models.UniqueConstraint(fields=['service', 'user'], name='unique_user_service_report'),
            models.UniqueConstraint(fields=['service', 'ip_address'], name='unique_ip_service_report'),
        ]

    def __str__(self):
        return f"Flag of service {self.service.id} by {self.user or self.ip_address}"
