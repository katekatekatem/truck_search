from django_filters import rest_framework as filters

from trucks.models import Cargo


class CargoFilter(filters.FilterSet):
    min_weight = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    max_weight = filters.NumberFilter(field_name='weight', lookup_expr='lte')
    min_distance = filters.NumberFilter(
        field_name='pick_up',
        lookup_expr='gte'
    )
    max_distance = filters.NumberFilter(
        field_name='pick_up',
        lookup_expr='lte'
    )

    class Meta:
        model = Cargo
        fields = ['weight', 'pick_up']
