
import django_filters
from .models import Service

class ServiceFilter(django_filters.FilterSet):
    # category = django_filters.NumberFilter(field_name="category")
    service_category_slug = django_filters.CharFilter(field_name="service_categories__slug", lookup_expr="iexact")
    provider = django_filters.NumberFilter(field_name="provider")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Print the initial data for debugging
        print('ServiceFilter init data:', self.data)

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        service_category_slug = self.data.get('service_category_slug')
        if service_category_slug:
            print(f"Filtering by service_category_slug: {service_category_slug}")
            print(f"Resulting queryset count: {qs.count()}")
        return qs

    # class Meta:
    #     model = Service
    #     fields = ['category', 'provider']
    class Meta:
        model = Service
        fields = ['service_category_slug', 'provider']




