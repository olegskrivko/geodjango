# guides/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Guide
from .serializers import GuideListSerializer, GuideDetailSerializer

class GuideListView(generics.ListAPIView):
    queryset = Guide.objects.filter(is_visible=True).order_by('order')
    serializer_class = GuideListSerializer
    permission_classes = [AllowAny]

class GuideDetailView(generics.RetrieveAPIView):
    queryset = Guide.objects.filter(is_visible=True)
    serializer_class = GuideDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
