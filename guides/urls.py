# guides/urls.py
from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import GuideViewSet, ParagraphViewSet

# router = DefaultRouter()
# router.register(r'guides', GuideViewSet, basename='guides')

# guides_router = NestedDefaultRouter(router, r'guides', lookup='guide')
# guides_router.register(r'paragraphs', ParagraphViewSet, basename='guide-paragraphs')

router = DefaultRouter()
router.register(r'', GuideViewSet, basename='guides')  # <-- empty prefix, use '' instead of 'guides'

guides_router = NestedDefaultRouter(router, r'', lookup='guide')  # nested on root '' as well
guides_router.register(r'paragraphs', ParagraphViewSet, basename='guide-paragraphs')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(guides_router.urls)),
]

# NOTE:
# We do NOT use a separate ParagraphViewSet or nested route for paragraphs,
# because paragraphs are always accessed through the Guide detail endpoint,
# where paragraphs are included and already ordered by the 'order' field in the model Meta.
# This simplifies the API and frontend consumption since all paragraph data
# is returned nested inside the Guide detail response.
