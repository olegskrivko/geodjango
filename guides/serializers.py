# guides/serializers.py
from rest_framework import serializers
from .models import Guide, Paragraph

class ParagraphSerializer(serializers.ModelSerializer):
    illustration_url = serializers.SerializerMethodField()

    class Meta:
        model = Paragraph
        fields = ['id', 'order', 'step_title', 'content', 'illustration_url', 'illustration_alt']

    def get_illustration_url(self, obj):
        return obj.illustration.url if obj.illustration else None


class GuideListSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Guide
        fields = ['id', 'title', 'slug', 'cover_url', 'description']

    def get_cover_url(self, obj):
        return obj.cover.url if obj.cover else None


class GuideDetailSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()
    paragraphs = ParagraphSerializer(many=True, read_only=True)

    class Meta:
        model = Guide
        fields = ['id', 'title', 'slug', 'cover_url', 'description', 'paragraphs']

    def get_cover_url(self, obj):
        return obj.cover.url if obj.cover else None
