# feedback/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import FeedbackSerializer, TestimonialSerializer
from .models import Testimonial
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.filter(is_visible=True).order_by('-created_at')
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]