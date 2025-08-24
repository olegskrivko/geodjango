# populate_animal_types.py

from django.core.management.base import BaseCommand
from services.models import ServiceCategory

POPULAR_SERVICES_CATEGORIES = [
    'Sitting',
    'Walking', 
    'Grooming',  
    'Training', 
    'Boarding', 
    'Veterinary', 
    'Photography',  
    'Rescue',  
    'Supplies', 
    'Art',  
    'Burial',  
    'Transport',   
    'Breeders', 
    'Insurance', 
    'Miscellaneous',  

]

class Command(BaseCommand):
    help = "Populate the ServiceCategory table with the most popular service categories."

    def handle(self, *args, **kwargs):
        created = 0
        for service in POPULAR_SERVICES_CATEGORIES:
            obj, was_created = ServiceCategory.objects.get_or_create(name=service)
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {service}"))
            else:
                self.stdout.write(f"Already exists: {service}")
        self.stdout.write(self.style.SUCCESS(f"Done. {created} new service categories added."))
