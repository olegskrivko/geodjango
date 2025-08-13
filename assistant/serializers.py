# assistant/serializers.py
from rest_framework import serializers
from .models import Question, AnswerOption, Score

class ScoreSerializer(serializers.ModelSerializer):
    pet_type = serializers.CharField(source='pet_type.name')

    class Meta:
        model = Score
        fields = ['pet_type', 'value']

class AnswerOptionSerializer(serializers.ModelSerializer):
    scores = ScoreSerializer(many=True)

    class Meta:
        model = AnswerOption
        fields = ['id', 'text', 'scores']

class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']
