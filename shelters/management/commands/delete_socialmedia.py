from django.core.management.base import BaseCommand
from shelters.models import SocialMedia

class Command(BaseCommand):
    help = "Delete all SocialMedia records from the database"

    def handle(self, *args, **kwargs):
        count = SocialMedia.objects.count()
        if count == 0:
            self.stdout.write("No SocialMedia records found to delete.")
            return

        SocialMedia.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully deleted {count} SocialMedia records")) 