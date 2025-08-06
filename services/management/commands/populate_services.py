from django.core.management.base import BaseCommand
from faker import Faker
from decimal import Decimal
import random
from django.contrib.auth import get_user_model
from services.models import Service, Location, Review, WorkingHour, SocialMedia
from datetime import time
from core.choices import COUNTRY_CHOICES, COUNTRY_DIALING_CODE_CHOICES

fake = Faker("lv_LV")  # Latvian locale
User = get_user_model()

class Command(BaseCommand):
    help = "Generate fake pet-related services with multiple locations and images"

    def handle(self, *args, **kwargs):
        country_codes = [code for code, _ in COUNTRY_CHOICES]
        dialing_codes = [code for code, _ in COUNTRY_DIALING_CODE_CHOICES]
        PLATFORM_CHOICES = dict(SocialMedia.PLATFORM_CHOICES)
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("❌ No users found. Please create users first."))
            return

        def get_choice(choices):
            return random.choice([c[0] for c in choices])

        # Latvian cities and streets for more realistic data
        latvian_cities = [
            "Rīga", "Daugavpils", "Liepāja", "Jelgava", "Jūrmala", 
            "Ventspils", "Rēzekne", "Valmiera", "Jēkabpils", "Ogre",
            "Tukums", "Cēsis", "Salaspils", "Kuldīga", "Sigulda"
        ]
        
        latvian_streets = [
            "Brīvības iela", "Raiņa bulvāris", "Elizabetes iela", "Krišjāņa Barona iela",
            "Merkela iela", "Stabu iela", "Terbatas iela", "Dzirnavu iela", "Gertrūdes iela",
            "Lāčplēša iela", "Matīsa iela", "Tērbatas iela", "Valdemāra iela", "Vīlandes iela",
            "Avotu iela", "Dzelzavas iela", "Kārļa Ulmaņa gatve", "Mūkusalas iela"
        ]

        for _ in range(20):  # Create 20 services
            operating_name = fake.catch_phrase()
            legal_name = f"{fake.company()} Ltd."
            registration_number = fake.unique.bothify(text='########-#')  # e.g. 12345678-1
            established_at = fake.date_between(start_date="-30y", end_date="today")
        
            user = random.choice(users)
            description = fake.paragraph(nb_sentences=4)
            price = round(random.uniform(5, 100), 2)
            price_type = get_choice(Service.PRICE_TYPE_CHOICES)
            category = get_choice(Service.SERVICE_CATEGORIES)
            provider = get_choice(Service.PROVIDER_TYPES)
            
            # ContactMixin
            country_code = random.choice(dialing_codes)  # ✅ Just the integer dialing code
            national_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            email = fake.company_email()
            website_url = fake.url()
            
            # Create service with multiple locations
            service = Service.objects.create(
                operating_name=operating_name,
                legal_name=legal_name,
                registration_number=registration_number,
                established_at=established_at,
                user=user,
                description=description,
                price=price,
                price_type=price_type,
                category=category,
                is_active=True,
                is_available=random.choice([True, False]),
                provider=provider,
                service_image_1="https://picsum.photos/600/400",
                service_image_2="https://picsum.photos/600/400",
                service_image_3="https://picsum.photos/600/400",
                service_image_4="https://picsum.photos/600/400",
                is_online=random.choice([True, False]),

                country_code=country_code,
                national_number=national_number,
                email=email,
                website_url=website_url,
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
                    service=service
                )

            # Create 1-3 locations per service
            num_locations = random.randint(1, 3)
            for loc_idx in range(num_locations):
                # city = random.choice(latvian_cities)
                # street = random.choice(latvian_streets)
                # street_number = random.randint(1, 100)

                # AddressMixin
                street_address = fake.street_address()
                street_address2 = fake.secondary_address()
                city = fake.city()
                state_or_province = fake.state()
                postal_code = fake.postcode()
                
                # Generate realistic Latvian coordinates
                # if city == "Rīga":
                #     lat = random.uniform(56.9, 57.0)
                #     lng = random.uniform(23.9, 24.2)
                # elif city == "Jelgava":
                #     lat = random.uniform(56.6, 56.7)
                #     lng = random.uniform(23.6, 23.8)
                # elif city == "Liepāja":
                #     lat = random.uniform(56.4, 56.6)
                #     lng = random.uniform(20.9, 21.1)
                # else:
                #     # General Latvia coordinates
                lat = random.uniform(56.0, 58.0)
                lng = random.uniform(20.5, 28.0)

                location = Location.objects.create(
                    service=service,
                    location_title=fake.company(),
                    location_description=fake.text(max_nb_chars=150),
                    
                    # AddressMixin
                    street_address=street_address,
                    street_address2=street_address2,
                    city=city,
                    state_or_province=state_or_province,
                    postal_code=postal_code,
                    latitude=lat,
                    longitude=lng,
                )

                # Create working hours for each location
                working_hours_data = [
                    (0, time(9, 0), time(17, 0)),  # Monday
                    (1, time(9, 0), time(17, 0)),  # Tuesday
                    (2, time(9, 0), time(17, 0)),  # Wednesday
                    (3, time(9, 0), time(17, 0)),  # Thursday
                    (4, time(9, 0), time(17, 0)),  # Friday
                    (5, time(10, 0), time(15, 0)),  # Saturday
                    (6, time(10, 0), time(15, 0)),  # Sunday
                ]

                for day, from_hour, to_hour in working_hours_data:
                    WorkingHour.objects.create(
                        location=location,
                        day=day,
                        from_hour=from_hour,
                        to_hour=to_hour,
                    )

            # Create some reviews for the service
            num_reviews = random.randint(0, 5)
            reviewed_users = set()  # Track users who have already reviewed this service
            
            for _ in range(num_reviews):
                # Get all users except the service owner and those who already reviewed
                available_users = [u for u in users if u != user and u not in reviewed_users]
                
                if not available_users:
                    break  # No more users available to review
                
                review_user = random.choice(available_users)
                reviewed_users.add(review_user)  # Mark this user as having reviewed
                
                Review.objects.create(
                    service=service,
                    user=review_user,
                    rating=Decimal(str(random.randint(1, 5))),
                    comment=fake.text(max_nb_chars=200),
                )

        self.stdout.write(
            self.style.SUCCESS(f"✅ Successfully created 20 services with multiple locations and reviews!")
        )
