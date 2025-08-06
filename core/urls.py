from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet
from django.urls import path, include
from .views import FAQListView, UserLocationAPIView
router = DefaultRouter()
router.register(r'', AnimalViewSet, basename='animal')

urlpatterns = [
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path("set-location/", UserLocationAPIView.as_view(), name="set-location"),
    path('', include(router.urls)),

]


