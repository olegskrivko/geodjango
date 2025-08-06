# populate_animal_types.py

from django.core.management.base import BaseCommand
from shelters.models import AnimalType

POPULAR_ANIMAL_TYPES = [
    "Dog",
    "Cat",
    "Parrot",
    "Rabbit",
    "Hamster",
    "Guinea Pig",
    "Turtle",
    "Fish",
    "Ferret",
    "Mouse",
    "Rat",
    "Snake",
    "Lizard",
    "Frog",
    "Chinchilla",
    "Hedgehog",
    "Bird",
    "Horse",
    "Goat",
    "Sheep",
    "Pig",
    "Chicken",
    "Duck",
    "Gecko",
    "Tarantula",
    "Hermit Crab",
    "Sugar Glider",
    "Tortoise",
    "Axolotl",
    "Salamander",
    "Other",
]

class Command(BaseCommand):
    help = "Populate the AnimalType table with the most popular pet types."

    def handle(self, *args, **kwargs):
        created = 0
        for animal in POPULAR_ANIMAL_TYPES:
            obj, was_created = AnimalType.objects.get_or_create(name=animal)
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Added: {animal}"))
            else:
                self.stdout.write(f"Already exists: {animal}")
        self.stdout.write(self.style.SUCCESS(f"Done. {created} new animal types added."))
