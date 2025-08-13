from django.core.management.base import BaseCommand
from feedback.models import Feedback

class Command(BaseCommand):
    help = "Delete all feedback entries"

    def handle(self, *args, **options):
        count = Feedback.objects.count()
        Feedback.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Deleted all {count} feedback entries."))
