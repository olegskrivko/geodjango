# feedback/urls.py
from django.urls import path
from .views import FeedbackCreateView

urlpatterns = [
    path('', FeedbackCreateView.as_view(), name='send-feedback'),
]
# # testimonials/urls.py
# from django.urls import path
# from .views import TestimonialListView

# urlpatterns = [
#     path('', TestimonialListView.as_view(), name='testimonial-list'),
# ]