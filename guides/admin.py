# from django.contrib import admin
# from .models import Guide, Paragraph

# class ParagraphInline(admin.TabularInline):
#     model = Paragraph
#     extra = 1  # Number of empty paragraph forms shown by default
#     fields = ('order', 'step_title', 'illustration', 'content', 'illustration_prompt')  # Customize fields shown inline
#     readonly_fields = []  # You can add readonly fields if needed

# class GuideAdmin(admin.ModelAdmin):
#     inlines = [ParagraphInline]
#     list_display = ('title', 'author', 'public', 'created_at', 'updated_at')
#     list_filter = ('public', 'created_at', 'author')
#     search_fields = ('title', 'description', 'author__username')
#     prepopulated_fields = {"slug": ("title",)}  # Auto-generate slug from title
#     ordering = ('-created_at',)
#     list_per_page = 20

# admin.site.register(Guide, GuideAdmin)
from django.contrib import admin
from .models import Guide, Paragraph

class ParagraphInline(admin.TabularInline):
    model = Paragraph
    extra = 1
    fields = ('order', 'step_title', 'illustration', 'content', 'illustration_prompt')
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')

class GuideAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]
    list_display = ('title', 'created_by', 'updated_by', 'is_visible', 'created_at', 'updated_at')
    list_filter = ('is_visible', 'created_at', 'created_by')
    search_fields = ('title', 'description', 'created_by__username')
    prepopulated_fields = {"slug": ("title",)}
    ordering = ('-created_at',)
    list_per_page = 20
    readonly_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Guide, GuideAdmin)
