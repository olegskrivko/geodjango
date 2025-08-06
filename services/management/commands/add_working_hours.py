from django.core.management.base import BaseCommand
from services.models import Location, WorkingHour
from datetime import time

class Command(BaseCommand):
    help = "Add working hours to existing locations that don't have them"

    def handle(self, *args, **kwargs):
        locations_without_hours = Location.objects.filter(working_hours__isnull=True)
        
        if not locations_without_hours.exists():
            self.stdout.write(self.style.SUCCESS("✅ All locations already have working hours."))
            return

        # Default working hours (Monday to Friday, 9:00-17:00)
        default_working_hours = [
            (0, time(9, 0), time(17, 0)),  # Monday
            (1, time(9, 0), time(17, 0)),  # Tuesday
            (2, time(9, 0), time(17, 0)),  # Wednesday
            (3, time(9, 0), time(17, 0)),  # Thursday
            (4, time(9, 0), time(17, 0)),  # Friday
        ]

        created_count = 0
        for location in locations_without_hours:
            for day, from_hour, to_hour in default_working_hours:
                WorkingHour.objects.get_or_create(
                    location=location,
                    day=day,
                    defaults={
                        'from_hour': from_hour,
                        'to_hour': to_hour
                    }
                )
            created_count += 1
            self.stdout.write(f"✅ Added working hours to location: {location.location_title}")

        self.stdout.write(
            self.style.SUCCESS(f"🎉 Successfully added working hours to {created_count} locations")
        ) 