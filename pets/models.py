from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField
from core.mixins import AddressMixin, ContactMixin

class Pet(AddressMixin, models.Model):
    STATUS_CHOICES = [
        (1, 'Lost'),
        (2, 'Found'),
        (3, 'Seen'),
    ]
    SPECIES_CHOICES = [
        (1, 'Dog'), 
        (2, 'Cat'), 
        (3, 'Other'),
    ]
    SIZE_CHOICES = [
        (1, 'Small'),
        (2, 'Medium'),
        (3, 'Large'),
    ]
    GENDER_CHOICES = [
        (1, 'Male'),
        (2, 'Female'),
    ]
    AGE_CHOICES = [
        (1, 'Young'), 
        (2, 'Adult'), 
        (3, 'Senior'),
    ]
    PATTERN_CHOICES = [
        (1, 'Solid'),
        (2, 'Striped'), 
        (3, 'Spotted'), 
        (4, 'Patched'), 
        (5, 'Marbled'),
    ]
    COLOR_CHOICES = [
        (1, 'Black'), 
        (2, 'Gray'), 
        (3, 'White'), 
        (4, 'Cream'), 
        (5, 'Yellow'), 
        (6, 'Golden'), 
        (7, 'Brown'), 
        (8, 'Red'), 
        (9, 'Lilac'), 
        (10, 'Blue'), 
        (11, 'Green'), 
        (12, 'Khaki'), 
        (13, 'Beige'), 
        (14, 'Fawn'), 
        (15, 'Chestnut'), 
    ]
    PHONE_CODE_CHOICES = [
        (1, 'United States (+1)'),
        (31, 'Netherlands (+31)'),
        (33, 'France (+33)'),
        (34, 'Spain (+34)'),
        (39, 'Italy (+39)'),
        (41, 'Switzerland (+41)'),
        (44, 'United Kingdom (+44)'),
        (46, 'Sweden (+46)'),
        (48, 'Poland (+48)'),
        (49, 'Germany (+49)'),
        (370, 'Lithuania (+370)'),
        (371, 'Latvia (+371)'),
        (372, 'Estonia (+372)'),
    ]
    FINAL_STATUS_CHOICES = [
        (1, 'Unresolved'),    
        (2, 'Reunited with Owner'), 
        (3, 'Given to Shelter'),   
        (4, 'Kept by finder'),      
        (5, 'Stray'),         
        (6, 'Free walk'),  
        (7, 'Found deceased'),     
        (8, 'Pet was found by owner'), 
        (9, 'Other'),   
    ]
    
    status = models.IntegerField(choices=STATUS_CHOICES, blank=False, null=False, verbose_name="Status")
    species = models.IntegerField(choices=SPECIES_CHOICES, blank=False, null=False, verbose_name="Species")
    size = models.IntegerField(choices=SIZE_CHOICES, blank=True, null=True, verbose_name="Size")
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True, verbose_name="Gender")
    age = models.IntegerField(choices=AGE_CHOICES, blank=True, null=True, verbose_name="Age")
    pattern = models.IntegerField(choices=PATTERN_CHOICES, blank=True, null=True, verbose_name="Pattern")
    primary_color = models.IntegerField(choices=COLOR_CHOICES, blank=True, null=True, verbose_name="Primary Color")
    secondary_color = models.IntegerField(choices=COLOR_CHOICES, blank=True, null=True, verbose_name="Secondary Color")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="Contact Phone")
    phone_code = models.IntegerField(choices=PHONE_CODE_CHOICES, blank=True, null=True, verbose_name="Phone Code")
    breed = models.CharField(max_length=255, blank=True, null=True, verbose_name="Breed")

    pet_image_1 = models.URLField(max_length=255, null=False, blank=False, verbose_name="Pet Image_1")
    pet_image_2 = models.URLField(max_length=255, null=True, blank=True, verbose_name="Pet Image_2")
    pet_image_3 = models.URLField(max_length=255, null=True, blank=True, verbose_name="Pet Image_3")
    pet_image_4 = models.URLField(max_length=255, null=True, blank=True, verbose_name="Pet Image_4")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    event_occurred_at = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Event Occurred At")
    is_public = models.BooleanField(default=True, verbose_name="Is Public?")
    is_closed = models.BooleanField(default=False, verbose_name="Is Closed?")
    is_archived = models.BooleanField(default=False, verbose_name="Is Archived?")
    is_banned = models.BooleanField(default=False, verbose_name="Is Banned?")
    final_status = models.IntegerField(choices=FINAL_STATUS_CHOICES, default=1, verbose_name="Final Status")
    
   

    def save(self, *args, **kwargs):
        # Auto-close only if the final_status is changed to something other than 1 ("Unresolved")
        self.is_closed = self.final_status != 1 
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"


    def __str__(self):
        return f"Pet {self.id}"
    
    

class PetSightingHistory(models.Model):
    STATUS_CHOICES = [
        (1, 'Found'), # Found
        (2, 'Seen'), # Seen
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=2, verbose_name="Status")
    #event_occurred_at = models.DateTimeField(default=timezone.now, blank=True, null=True, verbose_name="Notikuma laiks")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='sightings_history')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="latitude")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="longitude")

    # latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Ģeogrāfiskais platums")
    # longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Ģeogrāfiskais garums")
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="reporter")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    pet_image = models.URLField(max_length=255, null=True, blank=True, verbose_name="pet_image")
    is_public = models.BooleanField(default=True, verbose_name="Is Public?")


    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sighting"
        verbose_name_plural = "Sightings"

    def __str__(self):
        return f"{self.pet.id} - {self.get_status_display()} at {self.created_at}"

class Poster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='posters')
    name = models.CharField(max_length=255, blank=True)  # e.g. "Park fence poster"
    scans = models.PositiveIntegerField(default=0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    has_location = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class UserFavorites(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="favorited_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['user', 'pet'], name='unique_user_pet')
    ]

    def __str__(self):
        return f"{self.user.username} - {self.pet.id}"




class PetView(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='views')
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
        verbose_name = "Pet View"
        verbose_name_plural = "Pet Views"
        ordering = ['-created_at']

    def __str__(self):
        return f"View of Pet {self.pet.id} by {self.user or self.ip_address}"

class PetShare(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='shares')
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
        verbose_name = "Pet Share"
        verbose_name_plural = "Pet Shares"
        ordering = ['-created_at']

    def __str__(self):
        return f"Share of Pet {self.pet.id} by {self.user or self.ip_address} via {self.method}"

class PetReport(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='reports')
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
        verbose_name = "Pet Report"
        verbose_name_plural = "Pet Reports"
        ordering = ['-created_at']
        # Ensure one report per user/IP per pet
        constraints = [
            models.UniqueConstraint(fields=['pet', 'user'], name='unique_user_pet_report'),
            models.UniqueConstraint(fields=['pet', 'ip_address'], name='unique_ip_pet_report'),
        ]

    def __str__(self):
        return f"Flag of Pet {self.pet.id} by {self.user or self.ip_address}"

# class Animal(models.Model):
#     STATUS_CHOICES = [
#         (1, 'Available'),
#         (2, 'Adopted'),
#         (3, 'Fostered'),
#     ]

#     SPECIES_CHOICES = [
#         (1, 'Dog'),
#         (2, 'Cat'),
#         (3, 'Bird'),
#         (4, 'Other'),
#     ]

#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     species = models.IntegerField(choices=SPECIES_CHOICES)
#     status = models.IntegerField(choices=STATUS_CHOICES, default=1)
#     # image = CloudinaryField('image', blank=True, null=True)
#     image = models.URLField(blank=True, null=True)  # Store URL string only

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    

