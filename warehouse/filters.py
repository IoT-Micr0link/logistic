from django_filters import FilterSet, filters

from warehouse.models import WarehouseEntry, TransferOrder


class WarehouseEntryFilter(FilterSet):
    entry_date_min = filters.DateTimeFilter(field_name='entry_date', lookup_expr='date__gte')
    entry_date_max = filters.DateTimeFilter(field_name='entry_date', lookup_expr='date__lte')

    class Meta:
        model = WarehouseEntry
        fields = ('location', 'origin',)


class TransferOrderFilter(FilterSet):
    completion_date_min = filters.DateTimeFilter(field_name='actual_completion_date', lookup_expr='date__gte')
    completion_date_max = filters.DateTimeFilter(field_name='actual_completion_date', lookup_expr='date__lte')

    class Meta:
        model = TransferOrder
        fields = ('destination',)