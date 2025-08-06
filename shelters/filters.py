import django_filters
from .models import Shelter
from django.db.models import Q

class ShelterFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category")
    size = django_filters.NumberFilter(field_name="size")
    animal_type_slug = django_filters.CharFilter(field_name="animal_types__slug", lookup_expr="iexact")
    search = django_filters.CharFilter(method='filter_by_search', label='Search')

    def filter_by_search(self, queryset, name, value):
        terms = value.strip().split()
        for term in terms:
            queryset = queryset.filter(
                Q(description__icontains=term) | Q(operating_name__icontains=term)
            )
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Print the initial data for debugging
        print('ShelterFilter init data:', self.data)

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        animal_type_slug = self.data.get('animal_type_slug')
        if animal_type_slug:
            print(f"Filtering by animal_type_slug: {animal_type_slug}")
            print(f"Resulting queryset count: {qs.count()}")
        return qs

    class Meta:
        model = Shelter
        fields = ['search', 'category', 'size', 'animal_type_slug']
