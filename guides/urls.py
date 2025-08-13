# guides/urls.py
from django.urls import path
from .views import GuideListView, GuideDetailView

urlpatterns = [
    path('', GuideListView.as_view(), name='guide-list'),
    path('<slug:slug>/', GuideDetailView.as_view(), name='guide-detail'),
]
