# feedback/urls.py
from django.urls import path
from .views import FeedbackCreateView, TestimonialListView

urlpatterns = [
    path('', FeedbackCreateView.as_view(), name='send-feedback'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list')
]
