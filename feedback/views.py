# feedback/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import FeedbackSerializer

class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
