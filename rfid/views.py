from django.views import generic
from django_tables2 import SingleTableView, SingleTableMixin
from rfid.tables import *
from rfid.filters import *
from rfid.forms import *
from django.db.models import Count


class ItemInventoryView(SingleTableView):
    model = InventorySummary
    template_name = 'dashboard/logistics/inventory/inventory_by_item.html'
    table_class = InventorySummaryTable
    filterset_class = InventorySummaryFilter
    filterset_form = InventorySummaryFilterForm
    table_pagination = {
        'per_page': 30
    }

    def get_table_data(self):
        return self.filterset_class(self.request.GET, queryset=InventorySummary.objects.all()).qs

    def get_context_data(self, **kwargs):
        context = super(ItemInventoryView, self).get_context_data(**kwargs)
        form = self.filterset_form(self.request.GET or None)
        filter = self.filterset_class(self.request.GET, queryset=InventorySummary.objects.all())
        context["form"] = form
        context["filter"] = filter
        return context


class LocationInventoryView(SingleTableView):
    model = InventorySummary
    template_name = 'dashboard/logistics/inventory/inventory_by_location.html'
    table_class = InventorySummaryTable
    filterset_class = InventorySummaryFilter
    filterset_form = InventorySummaryFilterForm
    table_pagination = {
        'per_page': 30
    }

    def get_table_data(self):
        return self.filterset_class(self.request.GET, queryset=InventorySummary.objects.all()).qs

    def get_context_data(self, **kwargs):
        context = super(LocationInventoryView, self).get_context_data(**kwargs)
        form = self.filterset_form(self.request.GET or None)
        filter = self.filterset_class(self.request.GET, queryset=InventorySummary.objects.all())
        context["form"] = form
        context["filter"] = filter
        return context


class SKUDetailView(SingleTableMixin,  generic.detail.DetailView):
    model = SKU
    template_name = 'dashboard/logistics/inventory/sku_detail.html'
    context_object_name = "sku_object"
    table_class = ItemTable
    filterset_class = ItemFilter
    table_pagination = {
        'per_page': 10
    }

    def get_table_data(self):
        return self.filterset_class(self.request.GET, queryset=Item.objects.filter(sku=self.object)).qs

    def get_context_data(self, **kwargs):
        context = super(SKUDetailView, self).get_context_data(**kwargs)
        filter = self.filterset_class(self.request.GET, queryset=Item.objects.filter(sku=self.object))
        context['location_id'] = self.request.GET.get('current_location')
        context['filter'] = filter
        context['locations_inventory_list'] = Item.objects.filter(sku=self.object).values('current_location_id', 'current_location__name')\
            .annotate(total=Count('current_location_id', distinct=False)).order_by('-total')

        return context


class SKUListView(SingleTableView):
    model = SKU
    template_name = 'dashboard/logistics/inventory/inventory_by_sku.html'
    table_class = SkuInventoryTable
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(SKUListView, self).get_context_data(**kwargs)
        context['total_items'] = Item.objects.all().count()
        context['total_locations'] = Location.objects.all().count()
        context['total_locations_in_use'] = Item.objects.all().values('current_location__id').distinct().count()
        context['total_referencias'] = SKU.objects.count()
        return context


class ReadingsListView(SingleTableView):
    model = Reading
    template_name = 'dashboard/rfid/readings_list.html'
    table_class = ReadingsTable
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(ReadingsListView, self).get_context_data(**kwargs)
        return context


class ReadersListView(SingleTableView):
    model = Reader
    template_name = 'dashboard/rfid/readers_list.html'
    table_class = ReaderTable
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(ReadersListView, self).get_context_data(**kwargs)
        context['total_nodes'] = Node.objects.all().count()
        context['total_readers'] = Reader.objects.all().count()
        context['total_antennas'] = ReaderAntenna.objects.all().count()

        return context


class TransferOrderListView(SingleTableView):
    model = TransferOrder
    template_name = 'dashboard/logistics/transfers/transfer_order_list.html'
    table_class = TransferOrderTable
    filterset_class = TransferOrderFilter
    table_pagination = {
        'per_page': 30
    }

    def get_table_data(self):
        return self.filterset_class(self.request.GET, queryset=TransferOrder.objects.all()).qs

    def get_context_data(self, **kwargs):
        context = super(TransferOrderListView, self).get_context_data(**kwargs)
        context['total_orders'] = TransferOrder.objects.all().count()
        context['total_completed_orders'] = TransferOrder.objects.filter(state='CO').count()
        context['total_inprogress_orders'] = TransferOrder.objects.filter(state='IP').count()

        filter = self.filterset_class(self.request.GET, queryset=TransferOrder.objects.all())
        context['filter'] = filter
        return context


class TransferOrderDetailView(SingleTableView):
    template_name = 'dashboard/logistics/transfers/transfer_order_detail.html'
    model = TransferOrderItem
    table_class = TransferOrderItemTable
    table_pagination = {
        'per_page': 15
    }

    def get_queryset(self):
        qs = TransferOrderItem.objects.filter(order_id =self.kwargs['id_order'])
        return qs

    def get_context_data(self, **kwargs):
        context = super(TransferOrderDetailView, self).get_context_data(**kwargs)
        context['order_object'] = TransferOrder.objects.filter(id=self.kwargs['id_order']).first()
        total_items_enlisted = self.get_queryset().filter(state='AL').count()
        items_count = self.get_queryset().count()
        enlisted_items_per = total_items_enlisted * 100 / items_count

        context['enlisted_items_count'] = total_items_enlisted
        context['items_count'] = items_count
        context['enlisted_items_per'] = enlisted_items_per


        return context


class WarehouseEntryListView(SingleTableView):
    model = WarehouseEntry
    template_name = 'dashboard/logistics/transfers/warehouse_entry_list.html'
    table_class = WarehouseEntryTable
    filterset_class = WarehouseEntryFilter
    table_pagination = {
        'per_page': 30
    }

    def get_table_data(self):
        return self.filterset_class(self.request.GET, queryset=WarehouseEntry.objects.all()).qs

    def get_context_data(self, **kwargs):
        context = super(WarehouseEntryListView, self).get_context_data(**kwargs)
        context['total_sku_today'] = WarehouseEntryItem.objects.all().values('item__sku').distinct().count()
        context['total_items_today'] = WarehouseEntryItem.objects.count()
        filter = self.filterset_class(self.request.GET, queryset=WarehouseEntry.objects.all())
        context['filter'] = filter

        return context


class WarehouseEntryDetailView(SingleTableView):
    template_name = 'dashboard/logistics/transfers/warehouse_entry_detail.html'
    model = WarehouseEntryItem
    table_class = WarehouseEntryItemTable
    table_pagination = {
        'per_page': 15
    }

    def get_queryset(self):
        qs = WarehouseEntryItem.objects.filter(entry_id=self.kwargs['id_entry'])
        return qs

    def get_context_data(self, **kwargs):
        context = super(WarehouseEntryDetailView, self).get_context_data(**kwargs)
        context['entry_object'] = WarehouseEntry.objects.filter(id=self.kwargs['id_entry']).first()
        context['items_count'] = self.get_queryset().count()
        return context


class TrackingTransfersView(generic.TemplateView):
    template_name = 'dashboard/logistics/tracking/tracking_transfer_orders.html'


class TrackingWarehouseView(generic.TemplateView):
    template_name = 'dashboard/logistics/tracking/tracking_warehouse.html'


    def get_context_data(self, **kwargs):
        context = super(TrackingWarehouseView, self).get_context_data(**kwargs)

        items = Item.objects.all().values_list('epc', flat=True)  # This is not efficent
        time_threshold = timezone.now() - timedelta(minutes=settings.RFID_READING_CYCLE)

        context['reading_summary_snapshot'] = LastReadingsSnapshot.objects.filter(
            timestamp_reading__gte=time_threshold,
            epc__in=items
        ).values('antenna', 'antenna__name') \
            .annotate(total=Count('antenna')).order_by('total')
        return context


#Autocompletes
class SKUAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SKU.objects.all()
        if self.q:
            qs = qs.filter(display_name__istartswith=self.q)
        return qs


class LocationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Location.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs