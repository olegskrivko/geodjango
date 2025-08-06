from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
import random
from django.contrib.auth import get_user_model

from guides.models import Guide, Paragraph

fake = Faker()
User = get_user_model()

class Command(BaseCommand):
    help = "Generate fake guides with paragraphs"

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("❌ No users found. Create a user first."))
            return

        for _ in range(10):  # Create 10 guides
            user = random.choice(users)
            title = fake.sentence(nb_words=6)
            description = fake.paragraph(nb_sentences=4)

            guide = Guide.objects.create(
                title=title,
                description=description,
                is_visible=random.choice([True, False]),
                cover_prompt=fake.sentence(nb_words=8),
                cover_alt=fake.sentence(nb_words=5),
                cover_caption=fake.sentence(nb_words=6),
                cover_source=fake.company(),
                created_by=user,
                updated_by=user,
            )

            paragraph_count = random.randint(2, 5)
            for i in range(paragraph_count):
                Paragraph.objects.create(
                    guide=guide,
                    order=i,
                    step_title=fake.sentence(nb_words=4),
                    content=fake.paragraph(nb_sentences=5),
                    illustration_prompt=fake.sentence(nb_words=7),
                    illustration_alt=fake.sentence(nb_words=5),
                    illustration_caption=fake.sentence(nb_words=6),
                    illustration_source=fake.company(),
                    created_by=user,
                    updated_by=user,
                )

            self.stdout.write(
                f"✅ Created guide: {guide.title} with {paragraph_count} paragraphs"
            )

        self.stdout.write(self.style.SUCCESS("🎉 Successfully generated 10 fake guides."))
