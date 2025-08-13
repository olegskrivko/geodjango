from django.core.management.base import BaseCommand
from assistant.models import PetType, Question, AnswerOption, Score

class Command(BaseCommand):
    help = "Seeds the pet quiz questions, answers, and scores"

    def handle(self, *args, **kwargs):
        data = [
            {
                "question": "How much space do you have for a pet?",
                "options": [
                    {"answer": "Small apartment", "scores": {"cat": 2, "dog": -1, "none": 0}},
                    {"answer": "Medium-sized house", "scores": {"cat": 1, "dog": 1, "none": 0}},
                    {"answer": "Large house with a yard", "scores": {"dog": 2, "cat": 0, "none": 0}},
                ],
            },
            {
                "question": "How active are you in your daily life?",
                "options": [
                    {"answer": "Very active, love sports", "scores": {"dog": 2, "cat": -1, "none": 0}},
                    {"answer": "Moderately active", "scores": {"dog": 1, "cat": 1, "none": 0}},
                    {"answer": "Not very active, prefer a calm life", "scores": {"cat": 2, "dog": -1, "none": 0}},
                ],
            },
            {
                "question": "How much time can you dedicate to pet care?",
                "options": [
                    {"answer": "A lot of free time", "scores": {"dog": 2, "cat": 1, "none": 0}},
                    {"answer": "Sometimes free time", "scores": {"cat": 2, "dog": 0, "none": 0}},
                    {"answer": "Very little time", "scores": {"none": 2, "dog": -1, "cat": -1}},
                ],
            },
            {
                "question": "Do you have children at home?",
                "options": [
                    {"answer": "Yes, small children", "scores": {"dog": 2, "cat": -1, "none": 0}},
                    {"answer": "Yes, older children", "scores": {"dog": 1, "cat": 1, "none": 0}},
                    {"answer": "No children", "scores": {"cat": 2, "dog": 0, "none": 0}},
                ],
            },
            {
                "question": "How often are you away from home?",
                "options": [
                    {"answer": "Rarely, mostly at home", "scores": {"dog": 2, "cat": 1, "none": 0}},
                    {"answer": "Sometimes", "scores": {"cat": 2, "dog": 0, "none": 0}},
                    {"answer": "Often away or traveling", "scores": {"none": 2, "dog": -1, "cat": -1}},
                ],
            },
            {
                "question": "What kind of environment do you prefer at home?",
                "options": [
                    {"answer": "Lively, noisy, active", "scores": {"dog": 2, "cat": -1, "none": 0}},
                    {"answer": "Balanced", "scores": {"dog": 1, "cat": 1, "none": 0}},
                    {"answer": "Quiet and peaceful", "scores": {"cat": 2, "dog": 0, "none": 0}},
                ],
            },
            {
                "question": "Do you or anyone in your household have allergies?",
                "options": [
                    {"answer": "Yes, sensitive to fur", "scores": {"none": 2, "cat": -1, "dog": -1}},
                    {"answer": "No allergies", "scores": {"dog": 1, "cat": 1, "none": 0}},
                ],
            },
            {
                "question": "How independent do you want your pet to be?",
                "options": [
                    {"answer": "Very independent", "scores": {"cat": 2, "dog": -1, "none": 0}},
                    {"answer": "Balanced", "scores": {"dog": 1, "cat": 1, "none": 0}},
                    {"answer": "Needs a lot of attention", "scores": {"dog": 2, "cat": 0, "none": 0}},
                ],
            },
            {
                "question": "What is your monthly budget for a pet?",
                "options": [
                    {"answer": "Low (up to €50)", "scores": {"cat": 2, "dog": -1, "none": 0}},
                    {"answer": "Medium (€50–100)", "scores": {"dog": 1, "cat": 1, "none": 0}},
                    {"answer": "High (more than €100)", "scores": {"dog": 2, "cat": 1, "none": 0}},
                ],
            },
        ]


        # Create pet types
        pet_types = {}
        for pet_name in ['dog', 'cat', 'none']:
            pet_type, _ = PetType.objects.get_or_create(name=pet_name)
            pet_types[pet_name] = pet_type

        # Clear existing data (optional safety step)
        Score.objects.all().delete()
        AnswerOption.objects.all().delete()
        Question.objects.all().delete()

        for item in data:
            question = Question.objects.create(text=item['question'])
            for option_data in item['options']:
                option = AnswerOption.objects.create(question=question, text=option_data['answer'])
                for pet, score in option_data['scores'].items():
                    Score.objects.create(answer_option=option, pet_type=pet_types[pet], value=score)

        self.stdout.write(self.style.SUCCESS("✅ Pet quiz data seeded successfully."))
