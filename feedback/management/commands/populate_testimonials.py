from django.core.management.base import BaseCommand
from feedback.models import Testimonial
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Fill the database with fake testimonials'

    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(10):
            testimonial = Testimonial.objects.create(
                text=fake.paragraph(nb_sentences=3),
                author_name=fake.name(),
                author_title=fake.job(),
                author_company=fake.company(),
                is_visible=random.choice([True, False])
            )
            self.stdout.write(self.style.SUCCESS(f"Created testimonial: {testimonial.author_name}"))

        self.stdout.write(self.style.SUCCESS("Successfully added 10 fake testimonials!"))
