# guides/views.py
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import AllowAny, BasePermission, SAFE_METHODS
from .models import Guide, Paragraph
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import GuideListSerializer, GuideDetailSerializer, ParagraphSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

class IsAdminOrReadOnly(BasePermission):
    """
    Allows read-only access to anyone.
    Write access is restricted to authenticated staff or superusers.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))


class GuideViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, creating, updating Guides.
    Only admin/staff can modify.
    """
    queryset = Guide.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        return Guide.objects.filter(is_visible=True)
    
    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        try:
            guide = Guide.objects.get(slug=slug, is_visible=True)
        except Guide.DoesNotExist:
            raise NotFound("Guide not found or not visible.")
        serializer = self.get_serializer(guide)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return GuideListSerializer
        return GuideDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ParagraphViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Paragraphs filtered by Guide slug.
    Returns paragraphs belonging to the guide identified by slug.
    """
    serializer_class = ParagraphSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        guide_slug = self.kwargs.get('guide_slug')  # from nested router
        return Paragraph.objects.filter(guide__slug=guide_slug).order_by('order')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
    


# class GuideViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for listing, retrieving, creating, updating Guides.
#     Uses slug as the lookup field.
#     Returns different serializers for list vs detail views.
#     """
#     queryset = Guide.objects.all()
#     # permission_classes = [permissions.AllowAny]
#     permission_classes = [AllowAny]
#     lookup_field = 'slug'   # use slug in URLs instead of numeric ID

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return GuideListSerializer
#         return GuideDetailSerializer


# class ParagraphViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for Paragraphs filtered by Guide slug.
#     Returns paragraphs belonging to the guide identified by slug.
#     """
#     serializer_class = ParagraphSerializer
#     permission_classes = [AllowAny]
#     # permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         guide_slug = self.kwargs.get('guide_slug')  # from nested router
#         return Paragraph.objects.filter(guide__slug=guide_slug).order_by('order')


# Common self.action types in a ViewSet
# self.action value	Meaning	HTTP method(s)
# list	Return a list of objects	GET /api/objects/
# retrieve	Return a single object (detail)	GET /api/objects/{id}/
# create	Create a new object	POST
# update	Update an entire object (PUT)	PUT
# partial_update	Partially update an object (PATCH)	PATCH
# destroy	Delete an object	DELETE