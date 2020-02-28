from django.views import generic
from django_tables2 import SingleTableView
from rfid.tables import *
from statistics import mean


class InventoryView(generic.TemplateView):
    template_name = 'dashboard/logistica/inventario.html'



class ItemListView(SingleTableView):
    model = Item
    template_name = 'dashboard/logistica/inventario.html'
    table_class = ItemTable
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['total_items'] = Item.objects.all().count()
        context['total_locations'] = Location.objects.all().count()
        context['average_age'] = mean([item.age for item in Item.objects.all()]) # this is not efficent, it should be a DB view

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
    template_name = 'dashboard/logistica/transfer_order_list.html'
    table_class = TransferOrderTable
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(TransferOrderListView, self).get_context_data(**kwargs)
        context['total_orders'] = TransferOrder.objects.all().count()
        context['total_completed_orders'] = TransferOrder.objects.filter(state='CO').count()
        context['total_incomplete_orders'] = TransferOrder.objects.filter(state='IN').count()
        return context


class TransferOrderDetailView(SingleTableView):
    template_name = 'dashboard/logistica/transfer_order_detail.html'
    model = TransferOrderItem
    table_class = TransferOrderItemTable
    table_pagination = {
        'per_page': 15
    }

    def get_queryset(self):
        qs = TransferOrderItem.objects.filter(order_id  =self.kwargs['id_order'])
        return qs

    def get_context_data(self, **kwargs):
        context = super(TransferOrderDetailView, self).get_context_data(**kwargs)
        context['order_object'] = TransferOrder.objects.filter(id=self.kwargs['id_order']).first()
        context['enlisted_items_count'] = self.get_queryset().filter(state='AL').count()
        context['completed_items_count'] = self.get_queryset().filter(state='EN').count()
        context['items_count'] = self.get_queryset().count()
        context['enlisted_items_per'] = context['enlisted_items_count'] * 100 / context['items_count']
        context['completed_items_per'] = context['completed_items_count'] * 100 / context['items_count']

        return context