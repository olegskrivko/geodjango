from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PushSubscriptionViewSet

router = DefaultRouter()
router.register(r'', PushSubscriptionViewSet, basename='push-subscription')

urlpatterns = [
    path('', include(router.urls)),
]
