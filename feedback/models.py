# feedback/models.py
from django.db import models
from django.conf import settings

class Feedback(models.Model):
    SUBJECT_CHOICES = [
        (1, 'General Questions'),
        (2, 'Bug Report'),
        (3, 'Feature Request'),
        (4, 'Collaboration Request'),
        (5, 'Other'),
    ]

    subject = models.PositiveSmallIntegerField(choices=SUBJECT_CHOICES, default=1, help_text="Choose the topic that best describes your feedback.")
    message = models.TextField(help_text="Write your feedback message here.")
    name = models.CharField(max_length=100, help_text="Enter your full name.")
    email = models.EmailField(help_text="Enter your email address so we can get back to you.")

    resolved = models.BooleanField(default=False, help_text="Mark if feedback has been addressed")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_created', help_text="User who created this feedback.")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback_updated', help_text="User who last updated this feedback.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the feedback was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the feedback was last updated.")

    def __str__(self):
        subject_display = dict(self.SUBJECT_CHOICES).get(self.subject, "Unknown")
        return f"{self.name} - {subject_display}"
    

# class Testimonial(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     text = models.TextField(help_text="The testimonial content.")
#     author_name = models.CharField(max_length=255, help_text="Full name of the person.")
#     author_title = models.CharField(max_length=255, blank=True, help_text="Job title of the person.")
#     author_company = models.CharField(max_length=255, blank=True, help_text="Company name.")
#     author_photo = models.ImageField(upload_to="testimonials/", blank=True, null=True, help_text="Optional author photo.")
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return f"{self.author_name} - {self.author_company or 'No Company'}"