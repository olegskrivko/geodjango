# # Register your models here.
# from django.contrib import admin
# from .models import FAQ

# @admin.register(FAQ)
# class FAQAdmin(admin.ModelAdmin):
#     list_display = ('question', 'is_active', 'order')
#     list_editable = ('is_active', 'order')

# core/admin.py
from django.contrib import admin
from .models import FAQ
from modeltranslation.admin import TranslationAdmin
import core.translation  # <- make sure the registration runs

@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ('question', 'is_active', 'order')
    list_editable = ('is_active', 'order')
