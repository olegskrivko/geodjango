# from django.db.models.signals import pre_save
# from django.dispatch import receiver
# from ..guides.models import Guide
# import cloudinary.api
# import cloudinary.exceptions

# @receiver(pre_save, sender=Guide)
# def update_cover_metadata_if_changed(sender, instance, **kwargs):
#     if not instance.pk or not instance.cover:
#         return

#     try:
#         # Get the previous cover image (if exists)
#         old_instance = Guide.objects.get(pk=instance.pk)
#         if old_instance.cover.public_id != instance.cover.public_id:
#             # The cover image has changed
#             meta = cloudinary.api.resource(instance.cover.public_id)

#             instance.cover_width = meta.get('width')
#             instance.cover_height = meta.get('height')
#             instance.cover_format = meta.get('format')
#             instance.cover_size = meta.get('bytes')

#     except Guide.DoesNotExist:
#         # New instance (no previous cover to compare)
#         pass
#     except cloudinary.exceptions.Error as e:
#         print(f"⚠️ Cloudinary metadata fetch failed: {e}")

# # 🧰 Most Common Signals
# # Signal	When it Fires
# # pre_save	Before .save() is called
# # post_save	After .save() is done
# # pre_delete	Before .delete() is called
# # post_delete	After .delete() is done