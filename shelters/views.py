# services/views.py
from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Shelter, AnimalType
from .serializers import ShelterSerializer, AnimalTypeSerializer
from .filters import ShelterFilter
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.auth import get_user_model
User = get_user_model()

class ShelterPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # Custom response structure with additional pagination metadata
        return Response({
            'count': self.page.paginator.count,
            'totalPages': self.page.paginator.num_pages,
            'currentPage': self.page.number,
            'results': data # Paginated result set (e.g. list of shelters)
        })

class ShelterViewSet(viewsets.ModelViewSet):
    queryset = Shelter.objects.filter(is_visible=True)
    serializer_class = ShelterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ShelterFilter
    pagination_class = ShelterPagination


    def get_queryset(self):
        queryset = super().get_queryset()

        # user defined coords
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        latitude = 56.9496   # Riga latitude
        longitude = 24.1052  # Riga longitude

        if latitude and longitude:
            try:
                user_location = Point(float(longitude), float(latitude), srid=4326)
                queryset = queryset.annotate(distance=Distance('location', user_location)).order_by('distance')
            except (ValueError, TypeError):
                pass  # Invalid input, ignore distance filtering

        return queryset
    

    # Override the default create behavior to automatically set created_by and updated_by fields
    def perform_create(self, serializer):
        """
        Called by DRF when a new Shelter instance is created.
        Automatically assigns the current authenticated user to both
        created_by and updated_by fields before saving.
        """
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    # Override the default update behavior to automatically update updated_by field
    def perform_update(self, serializer):
        """
        Called by DRF when an existing Shelter instance is updated.
        Automatically assigns the current authenticated user to the updated_by field
        before saving, keeping track of who last modified the shelter.
        """
        serializer.save(updated_by=self.request.user)

class AnimalTypeListView(generics.ListAPIView):
    """
    API view to list all Animal Types.
    - Returns all animal types ordered alphabetically by name.
    - Accessible to anyone (no authentication required).
    """
    queryset = AnimalType.objects.all().order_by('name')
    serializer_class = AnimalTypeSerializer
    permission_classes = [AllowAny]