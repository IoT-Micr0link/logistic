from django.views import generic
from django_tables2 import SingleTableView, SingleTableMixin
from rfid.tables import *
from rfid.view_models import *
from statistics import mean


class InventoryView(generic.TemplateView):
    template_name = 'dashboard/logistics/inventory/inventory_by_item.html'


class ItemListView(SingleTableView):
    model = Item
    template_name = 'dashboard/logistics/inventory/inventory_by_item.html'
    table_class = ItemTable
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['total_items'] = Item.objects.all().count()
        context['total_locations'] = Location.objects.all().count()
        context['average_age'] = mean([item.age for item in Item.objects.all()])    # this is not efficent, it should be
        return context                                                              # a DB view or batch process


class SKUDetailView(SingleTableMixin, generic.detail.DetailView ):
    model = SKU
    template_name = 'dashboard/logistics/inventory/sku_detail.html'
    context_object_name = "sku_object"
    table_class = ItemTable
    table_pagination = {
        'per_page': 10
    }

    def get_table_data(self):
        return Item.objects.filter(sku=self.object)

    def get_context_data(self, **kwargs):
        context = super(SKUDetailView, self).get_context_data(**kwargs)
        context['locations_inventory_list'] = InventorySummary.objects.filter(sku=self.object).select_related('last_seen_location')
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
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(TransferOrderListView, self).get_context_data(**kwargs)
        context['total_orders'] = TransferOrder.objects.all().count()
        context['total_completed_orders'] = TransferOrder.objects.filter(state='CO').count()
        context['total_inprogress_orders'] = TransferOrder.objects.filter(state='IP').count()
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
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(WarehouseEntryListView, self).get_context_data(**kwargs)
        context['total_items_year'] = WarehouseEntryItem.objects.count()
        context['total_items_month'] = WarehouseEntryItem.objects.count()
        context['total_items_today'] = WarehouseEntryItem.objects.count()

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