from django.core.management.base import BaseCommand
from core.models import FAQ  # Adjust if your model is elsewhere

class Command(BaseCommand):
    help = "Delete all FAQ entries"

    def handle(self, *args, **kwargs):
        count, _ = FAQ.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} FAQ entries."))
