from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal
from datetime import datetime
from shelters.models import Shelter, SocialMedia, AnimalType
from core.choices import COUNTRY_CHOICES, COUNTRY_DIALING_CODE_CHOICES

fake = Faker()

class Command(BaseCommand):
    help = "Generate 20 fake shelters with optional social media links and animal types"

    def handle(self, *args, **kwargs):
        country_codes = [code for code, _ in COUNTRY_CHOICES]
        dialing_codes = [code for code, _ in COUNTRY_DIALING_CODE_CHOICES]

        PLATFORM_CHOICES = dict(SocialMedia.PLATFORM_CHOICES)
        CATEGORY_CHOICES = [choice[0] for choice in Shelter.SHELTER_CATEGORY_CHOICES]
        SIZE_CHOICES = [choice[0] for choice in Shelter.SHELTER_SIZE_CHOICES]

        animal_types = list(AnimalType.objects.all())
        if not animal_types:
            self.stdout.write(self.style.ERROR("❌ No AnimalType objects found. Please populate AnimalType first."))
            return

        for _ in range(20):
            operating_name = f"{fake.company()} Shelter"
            legal_name = f"{fake.company()} Ltd."
            description = fake.text(max_nb_chars=200)
            registration_number = fake.unique.bothify(text='########-#')  # e.g. 12345678-1
            established_at = fake.date_between(start_date="-30y", end_date="today")
            size = random.choice(SIZE_CHOICES)
            category = random.choice(CATEGORY_CHOICES)
            is_visible = random.choice([True, False])
            is_offering_adoption = random.choice([True, False])
            is_accepting_volunteers = random.choice([True, False])
            is_accepting_donations = random.choice([True, False])
            country = random.choice(country_codes)  # ✅ Extracted just the country code string

            # ContactMixin
            country_code = random.choice(dialing_codes)  # ✅ Just the integer dialing code
            national_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            email = fake.company_email()
            website_url = fake.url()
            
            # AddressMixin
            street_address = fake.street_address()
            street_address2 = fake.secondary_address()
            city = fake.city()
            state_or_province = fake.state()
            postal_code = fake.postcode()
            
            # Coordinates based on country
            if country == 'LV':
                latitude = Decimal(random.uniform(55.6, 58.1))
                longitude = Decimal(random.uniform(20.9, 28.3))
            elif country == 'EE':
                latitude = Decimal(random.uniform(57.5, 59.7))
                longitude = Decimal(random.uniform(21.8, 28.2))
            elif country == 'LT':
                latitude = Decimal(random.uniform(53.9, 56.4))
                longitude = Decimal(random.uniform(20.6, 26.8))
            else:
                latitude = Decimal(random.uniform(55.6, 58.1))
                longitude = Decimal(random.uniform(20.9, 28.3))

            shelter = Shelter.objects.create(
                operating_name=operating_name,
                legal_name=legal_name,
                description=description,
                registration_number=registration_number,
                established_at=established_at,
                size=size,
                category=category,
                is_visible=is_visible,
                is_offering_adoption=is_offering_adoption,
                is_accepting_volunteers=is_accepting_volunteers,
                is_accepting_donations=is_accepting_donations,
                street_address=street_address,
                street_address2=street_address2,
                city=city,
                state_or_province=state_or_province,
                postal_code=postal_code,
                country=country,
                country_code=country_code,
                national_number=national_number,
                email=email,
                website_url=website_url,
                latitude=latitude,
                longitude=longitude,
            )

            num_socials = random.randint(0, 3)
            available_platforms = list(PLATFORM_CHOICES.keys())
            random.shuffle(available_platforms)
            
            for platform in available_platforms[:num_socials]:
                SocialMedia.objects.create(
                    platform=platform,
                    profile_url=fake.url(),
                    is_official=random.choice([True, False]),
                    is_verified=random.choice([True, False]),
                    shelter=shelter
                )

            selected_animal_types = random.sample(animal_types, k=random.randint(1, min(3, len(animal_types))))
            shelter.animal_types.add(*selected_animal_types)

            self.stdout.write(f"✅ Created shelter: {shelter.operating_name} with {len(selected_animal_types)} animal types")

        self.stdout.write(self.style.SUCCESS("🎉 Successfully created 20 fake shelters with all fields"))
