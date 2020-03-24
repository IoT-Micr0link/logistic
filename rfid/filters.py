from django_filters import  FilterSet, filters

from rfid.models import Item


class ItemFilter(FilterSet):
    last_seen_min = filters.DateTimeFilter(field_name='last_seen_timestamp', lookup_expr='date__gte' )
    last_seen_max = filters.DateTimeFilter(field_name='last_seen_timestamp', lookup_expr='date__lte')

    class Meta:
        model = Item
        fields = ('sku', 'last_seen_location', 'last_seen_action')