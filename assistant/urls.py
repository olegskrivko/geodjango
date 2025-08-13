# assistant/urls.py
from django.urls import path
from .views import ChatbotAPIView, PetRecommendationAPIView, PetQuizQuestionsAPIView

urlpatterns = [
    path('chatbot/', ChatbotAPIView.as_view(), name='chatbot'),
    path('pet-quiz/questions/', PetQuizQuestionsAPIView.as_view()),
    path('pet-quiz/analysis/', PetRecommendationAPIView.as_view()),
]
