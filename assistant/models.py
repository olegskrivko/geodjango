# assistant/models.py
from django.db import models

class PetType(models.Model):
    name = models.CharField(max_length=50)  # e.g., "dog", "cat", "none"

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"

class Score(models.Model):
    answer_option = models.ForeignKey(AnswerOption, on_delete=models.CASCADE, related_name='scores')
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE)
    value = models.IntegerField()  # e.g., -1, 0, 2
