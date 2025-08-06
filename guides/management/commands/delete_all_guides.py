from django.core.management.base import BaseCommand
from guides.models import Guide

class Command(BaseCommand):
    help = "Delete all guides and their related paragraphs"

    def handle(self, *args, **options):
        total = Guide.objects.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("⚠️ No guides found to delete."))
            return

        Guide.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"✅ Deleted {total} guides (and their paragraphs)."))
