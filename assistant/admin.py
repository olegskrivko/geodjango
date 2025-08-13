# assistant/admin.py
from django.contrib import admin
from .models import Question, AnswerOption, Score, PetType


class ScoreInline(admin.TabularInline):
    model = Score
    extra = 0
    autocomplete_fields = ['pet_type']


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 0
    show_change_link = True


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('text',)
    inlines = [AnswerOptionInline]


@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'question')
    search_fields = ('text',)
    list_filter = ('question',)
    inlines = [ScoreInline]
    autocomplete_fields = ['question']


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer_option', 'pet_type', 'value')
    list_filter = ('pet_type', 'answer_option__question')
    autocomplete_fields = ['answer_option', 'pet_type']


@admin.register(PetType)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
