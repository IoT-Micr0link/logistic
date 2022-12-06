from django_filters import FilterSet, filters
from rfid.models import *


class ItemFilter(FilterSet):
    last_seen_min = filters.DateTimeFilter(field_name='last_seen_timestamp', lookup_expr='date__gte')
    last_seen_max = filters.DateTimeFilter(field_name='last_seen_timestamp', lookup_expr='date__lte')

    class Meta:
        model = Item
        fields = ('sku', 'current_location', 'last_seen_action')


class ItemListFilter(FilterSet):
    id_from = filters.NumberFilter(field_name='epc', lookup_expr='gte')
    id_to = filters.NumberFilter(field_name='epc', lookup_expr='lte')

    class Meta:
        model = Item
        fields = {'epc'}


class SKUFilter(FilterSet):
    id_from = filters.NumberFilter(field_name='id', lookup_expr='gte')
    id_to = filters.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = SKU
        fields = {'id'}


class InventorySummaryFilter(FilterSet):
    sku_id = filters.NumberFilter(field_name='sku_id')
    sku_id_from = filters.NumberFilter(field_name='sku_id', lookup_expr='gte')
    sku_id_to = filters.NumberFilter(field_name='sku_id', lookup_expr='lte')
    location_id = filters.NumberFilter(field_name='current_location_id')
    location_id_from = filters.NumberFilter(field_name='current_location_id', lookup_expr='gte')
    location_id_to = filters.NumberFilter(field_name='current_location_id', lookup_expr='lte')
    all_locations = filters.CharFilter(field_name='all_locations', method='filter_all_locations')
    all_skus = filters.CharFilter(field_name='all_skus', method='filter_all_skus')

    def filter_all_locations(self, queryset, field_name, value):
        if value:
            return self.Meta.model.objects.all()
        else:
            return queryset

    def filter_all_skus(self, queryset, field_name, value):
        if value:
            return self.Meta.model.objects.all()
        else:
            return queryset

    class Meta:
        model = SKU
        fields = ('sku_id', 'sku_id_from', 'sku_id_to', 'all_skus',
                  'location_id', 'location_id_from', 'location_id_to', 'all_locations',)


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
