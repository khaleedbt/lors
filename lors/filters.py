import django_filters

from .models import CarModel


class CarModelFilter(django_filters.FilterSet):
    brand_name = django_filters.CharFilter(field_name='brand__name', lookup_expr='icontains')
    template_code = django_filters.CharFilter(lookup_expr='icontains')
    car_type = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CarModel
        fields = ['brand', 'brand_name', 'template_code', 'car_type']
