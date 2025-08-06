# guides/serializers.py
from rest_framework import serializers
from .models import Guide, Paragraph

class ParagraphSerializer(serializers.ModelSerializer):
    """
    Serializer for Paragraph model.
    Used to represent individual paragraphs in a guide,
    including order, content, and optional illustration.
    """
    illustration_url = serializers.SerializerMethodField()

    class Meta:
        model = Paragraph
        fields = ['id', 'order', 'content', 'illustration', 'illustration_url', 'illustration_alt', 'step_title']

    def get_illustration_url(self, obj):
        if obj.illustration:
            # CloudinaryField has .url property
            return obj.illustration.url
        return None

class GuideDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Guide model.
    Includes all guide details plus nested paragraphs.
    Suitable for guide detail views where you want full content.
    """
    slug = serializers.ReadOnlyField()
    cover_url = serializers.SerializerMethodField()
    paragraphs = ParagraphSerializer(many=True, read_only=True)

    class Meta:
        model = Guide
        fields = ['id', 'title', 'slug', 'cover', 'cover_url', 'description', 'is_visible', 'created_at', 'updated_at', 'paragraphs']

    def get_cover_url(self, obj):
        if obj.cover:
            # CloudinaryField has .url property
            return obj.cover.url
        return None


class GuideListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing guides.
    Includes main guide info but excludes paragraphs to keep response light.
    Suitable for guide list views.
    """
    slug = serializers.ReadOnlyField()
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Guide
        fields = ['id', 'title', 'slug', 'cover', 'cover_url', 'cover_alt', 'description', 'is_visible']

    def get_cover_url(self, obj):
        if obj.cover:
            # CloudinaryField has .url property
            return obj.cover.url
        return None
