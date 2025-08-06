# core/mixins.py
from django.utils.text import slugify
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import Point
from .choices import COUNTRY_CHOICES, COUNTRY_DIALING_CODE_CHOICES
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models.functions import Distance as DistanceFunc

class SlugAutoMixin(models.Model):
    class Meta:
        abstract = True

    def get_slug_source_field(self):
        return getattr(self, 'slug_source_field', 'title')

    def get_slug_field_name(self):
        return getattr(self, 'slug_field_name', 'slug')

    def generate_unique_slug(self):
        source_field = self.get_slug_source_field()
        slug_field = self.get_slug_field_name()

        source = getattr(self, source_field, None)
        if not source:
            return

        base_slug = slugify(source)
        slug = base_slug
        num = 1
        ModelClass = self.__class__

        while ModelClass.objects.filter(**{slug_field: slug}).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        setattr(self, slug_field, slug)

    def save(self, *args, **kwargs):
        slug_field = self.get_slug_field_name()
        source_field = self.get_slug_source_field()

        if not getattr(self, slug_field, None):
            self.generate_unique_slug()
        else:
            old = self.__class__.objects.filter(pk=self.pk).first()
            if old and getattr(old, source_field) != getattr(self, source_field):
                self.generate_unique_slug()

        super().save(*args, **kwargs)


class ImageMetaMixin(models.Model):
    image = CloudinaryField('image', blank=True, null=True, help_text="Primary image (Cloudinary).")
    image_prompt = models.TextField(blank=True, help_text="Optional prompt or description related to the image.")
    image_alt = models.CharField(max_length=255, blank=True, help_text="Alternative text for the image.")
    image_caption = models.CharField(max_length=255, blank=True, help_text="Caption or description for the image.")
    image_source = models.CharField(max_length=255, blank=True, help_text="Source or credit for the image.")
    image_width = models.PositiveIntegerField(null=True, blank=True, help_text="Width of the image in pixels.")
    image_height = models.PositiveIntegerField(null=True, blank=True, help_text="Height of the image in pixels.")
    image_format = models.CharField(max_length=50, blank=True, help_text="Image format (e.g., jpg, png).")
    image_size = models.PositiveIntegerField(null=True, blank=True, help_text="File size in bytes.")

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    street_address = models.CharField(max_length=255, blank=True, null=True, help_text="Street address, P.O. box, company name, c/o")
    street_address2 = models.CharField(max_length=255, blank=True, null=True, help_text="Apartment, suite, unit, building, floor, etc.")
    city = models.CharField(max_length=100, blank=True, null=True)
    state_or_province = models.CharField(max_length=100, blank=True, null=True, help_text="State, province, or region")
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True, null=True, help_text="ISO 3166-1 alpha-2 country code")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location = geomodels.PointField(geography=True, blank=True, null=True)

    @property
    def full_address(self):
        parts = [
            self.street_address,
            self.street_address2,
            self.city,
            self.state_or_province,
            self.postal_code,
            self.get_country_display() if self.country else None
        ]
        return ", ".join(filter(None, parts))

    @property
    def distance_from_riga_km(self):
        if not self.location:
            return None

        riga_location = Point(24.1052, 56.9496, srid=4326)

        distance = self.__class__.objects.annotate(
            dist=DistanceFunc('location', riga_location)
        ).filter(id=self.id).values_list('dist', flat=True).first()

        if distance is not None:
            return round(distance.m / 1000, 2)  # distance is a Distance object
        return None    
    # @property
    # def distance_from_riga_km(self):
    #     if not self.location:
    #         return None

    #     riga_location = Point(24.1052, 56.9496, srid=4326)

    #     qs = self.__class__.objects.annotate(
    #         distance=DistanceFunc('location', riga_location)
    #     ).filter(id=self.id).values_list('distance', flat=True)

    #     if qs.exists():
    #         return round(qs.first().m / 1000, 2) if qs.exists() else None

    #     return None
    
    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude), srid=4326)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True

    def __str__(self):
        return self.full_address or "No address"


class ContactMixin(models.Model):
    country_code = models.PositiveIntegerField(
        choices=COUNTRY_DIALING_CODE_CHOICES,
        blank=True,
        null=True,
        help_text="Country dialing code without plus sign, e.g., 371"
    )
    national_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Local phone number without country code"
    )
    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Primary contact email address"
    )
    website_url = models.URLField(
        blank=True,
        null=True,
        help_text="Official website URL"
    )

    @property
    def full_phone_number(self):
        if self.country_code and self.national_number:
            return f"+{self.country_code}{self.national_number}"
        return None


    class Meta:
        abstract = True
