# feedback/admin.py
from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'get_subject_display', 'created_at', 'updated_at', 'resolved', 'created_by')
    list_filter = ('subject', 'resolved', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def get_subject_display(self, obj):
        return dict(Feedback.SUBJECT_CHOICES).get(obj.subject, "Unknown")
    get_subject_display.short_description = 'Subject'

admin.site.register(Feedback, FeedbackAdmin)
