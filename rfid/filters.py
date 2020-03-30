from django_filters import  FilterSet, filters

from rfid.models import Item, WarehouseEntry, TransferOrder


class ItemFilter(FilterSet):
    last_seen_min = filters.DateTimeFilter(field_name='last_seen_timestamp', lookup_expr='date__gte' )
    last_seen_max = filters.DateTimeFilter(field_name='last_seen_timestamp', lookup_expr='date__lte')

    class Meta:
        model = Item
        fields = ('sku', 'last_seen_location', 'last_seen_action')


class WarehouseEntryFilter(FilterSet):
    entry_date_min = filters.DateTimeFilter(field_name='entry_date', lookup_expr='date__gte' )
    entry_date_max = filters.DateTimeFilter(field_name='entry_date', lookup_expr='date__lte')

    class Meta:
        model=WarehouseEntry
        fields = ('location', 'origin',)


class TransferOrderFilter(FilterSet):
    completion_date_min = filters.DateTimeFilter(field_name='actual_completion_date', lookup_expr='date__gte' )
    completion_date_max = filters.DateTimeFilter(field_name='actual_completion_date', lookup_expr='date__lte')

    class Meta:
        model = TransferOrder
        fields = ('destination', )