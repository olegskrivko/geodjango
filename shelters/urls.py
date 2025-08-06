from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShelterViewSet, AnimalTypeListView

router = DefaultRouter()
router.register(r'', ShelterViewSet)
urlpatterns = [
    path('animal-types/', AnimalTypeListView.as_view(), name='animal-type-list'),
    path('', include(router.urls)),
]

