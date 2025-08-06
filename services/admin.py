from django.contrib import admin
from .models import Service, Review, Location, WorkingHour

# Inline for WorkingHour inside Location
class WorkingHourInline(admin.TabularInline):
    model = WorkingHour
    extra = 1


# Inline for Location inside Service
class LocationInline(admin.TabularInline):
    model = Location
    extra = 1
    show_change_link = True  # Enables "Edit" link to access Location admin

# Admin for Service with Location inlines
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('operating_name', 'category', 'created_at')
    search_fields = ('operating_name',)
    list_filter = ('category',)
    inlines = [LocationInline]


# Admin for Location with WorkingHour inlines
class LocationAdmin(admin.ModelAdmin):
    list_display = ('service', 'city',)
    inlines = [WorkingHourInline]

# Register everything
admin.site.register(Service, ServiceAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(WorkingHour)
admin.site.register(Review)