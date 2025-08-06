from django.core.management.base import BaseCommand
from shelters.models import AnimalType

class Command(BaseCommand):
    help = "Delete all AnimalType records from the database."

    def handle(self, *args, **kwargs):
        count = AnimalType.objects.count()
        if count == 0:
            self.stdout.write("No AnimalType records found to delete.")
            return
        AnimalType.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully deleted {count} AnimalType records.")) 