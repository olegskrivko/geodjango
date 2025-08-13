from django.core.management.base import BaseCommand
from faker import Faker
import random
from django.contrib.auth import get_user_model

from feedback.models import Feedback

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = "Generate fake feedback entries"

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake feedback entries to create (default: 10)',
        )

    def handle(self, *args, **options):
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("❌ No users found. Create users first."))
            return

        count = options['count']
        for _ in range(count):
            user = random.choice(users)
            Feedback.objects.create(
                subject=random.choice([1, 2, 3, 4, 5]),
                message=fake.paragraph(nb_sentences=5),
                name=fake.name(),
                email=fake.email(),
                resolved=random.choice([True, False]),
                created_by=user,
                updated_by=user,
            )
        self.stdout.write(self.style.SUCCESS(f"🎉 Successfully generated {count} fake feedback entries."))
