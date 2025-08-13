from django.core.management.base import BaseCommand
from assistant.models import PetType, Question, AnswerOption, Score

class Command(BaseCommand):
    help = "Deletes all pet quiz data from PetType, Question, AnswerOption, and Score tables"

    def handle(self, *args, **kwargs):
        # Delete order matters due to foreign key constraints
        Score.objects.all().delete()
        AnswerOption.objects.all().delete()
        Question.objects.all().delete()
        PetType.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("🗑️ All pet quiz data deleted successfully."))
