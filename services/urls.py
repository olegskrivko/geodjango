# services/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet,  ReviewListCreateView,ServiceCategoryListView,  service_view_stats, track_service_share, flag_service, unflag_service, get_service_flag_status, service_post_quota   # ServiceDetailView,

router = DefaultRouter()
router.register(r'', ServiceViewSet)  # Register ServiceViewSet for the list of services

urlpatterns = [
    path('service-categories/', ServiceCategoryListView.as_view(), name='service-category-list'),
    path('<int:service_id>/view-stats/', service_view_stats, name='service-view-stats'),
    path('<int:service_id>/track-share/', track_service_share, name='track-service-share'),
    path('<int:service_id>/flag/', flag_service, name='flag-service'),
    path('<int:service_id>/unflag/', unflag_service, name='unflag-service'),
    path('<int:service_id>/flag-status/', get_service_flag_status, name='get-service-flag-status'),
    path('service-quota/', service_post_quota, name='service-post-quota'),
    path('', include(router.urls)),  # Register the ServiceViewSet URLs under `/api/services/`
    # path('<int:id>/', ServiceDetailView.as_view(), name='service-detail'),  # Individual service detail view
    path('<int:service_id>/reviews/', ReviewListCreateView.as_view(), name='service-reviews'),


]



