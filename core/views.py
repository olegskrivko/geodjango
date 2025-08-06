# core/views.py
from rest_framework import viewsets
from .models import Animal
from .serializers import AnimalSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Point



class UserLocationAPIView(APIView):
    def post(self, request):
        lat = request.data.get("latitude")
        lng = request.data.get("longitude")
        if lat and lng:
            point = Point(float(lng), float(lat), srid=4326)
            # Use this point for filtering or calculation, e.g.:
            # shelters = Shelter.objects.annotate(
            #     distance=DistanceFunc('location', point)
            # ).filter(distance__lt=50000).order_by('distance')

            return Response({"detail": "Location received."})
        return Response({"error": "Missing coordinates."}, status=status.HTTP_400_BAD_REQUEST)

class AuditViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
     

class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.filter(is_active=True).order_by('order')
    serializer_class = FAQSerializer
    permission_classes = [AllowAny]

