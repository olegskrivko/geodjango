from rest_framework import serializers

from django.contrib.auth import get_user_model
from .models import FAQ
from .models import Animal
User = get_user_model()

class AnimalSerializer(serializers.ModelSerializer):
    image = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = Animal
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']
