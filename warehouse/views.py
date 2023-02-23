from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django_tables2 import SingleTableView

from inventory.models import Item
from rfid.view_models import LastReadingsSnapshot
from warehouse.filters import TransferOrderFilter, WarehouseEntryFilter
from warehouse.forms import CreateTransferOrderForm
from warehouse.models import TransferOrder, TransferOrderItem, WarehouseEntryItem, WarehouseEntry
from warehouse.tables import TransferOrderTable, TransferOrderItemTable, WarehouseEntryTable, WarehouseEntryItemTable


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
        qs = TransferOrderItem.objects.filter(order_id=self.kwargs['id_order'])
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


class CreateTransferOrder(CreateView):
    template_name = 'dashboard/logistics/transfers/modals/create_transfer_order.html'
    form_class = CreateTransferOrderForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            return HttpResponse()
        form.save()
        return redirect(to='logistics:transfer-order-list')


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


class TrackingTransfersView(TemplateView):
    template_name = 'dashboard/logistics/tracking/tracking_transfer_orders.html'


class TrackingWarehouseView(TemplateView):
    template_name = 'dashboard/logistics/tracking/tracking_warehouse.html'

    def get_context_data(self, **kwargs):
        context = super(TrackingWarehouseView, self).get_context_data(**kwargs)

        items = Item.objects.all().values_list('epc', flat=True)  # This is not efficient
        time_threshold = timezone.now() - timedelta(seconds=settings.RFID_READING_CYCLE)

        context['reading_summary_snapshot'] = LastReadingsSnapshot.objects.filter(
            epc__in=items,
            antenna_id__in=[1, 3],
        ).values('antenna', 'antenna__name').annotate(
            total=Count('antenna', filter=Q(timestamp_reading__gte=time_threshold))
        ).order_by('total')
        return context
