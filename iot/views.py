from django.views.generic import TemplateView
from rfid.models import Item, SKU, WarehouseEntry, TransferOrder, TransferOrderItem


class DashboardView(TemplateView):
    template_name = 'dashboard/logistics/logistics_index.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['total_items'] = Item.objects.filter(last_seen_action='READ').count()
        context['total_sku'] = SKU.objects.all().count()
        context['total_warehouseentries'] = WarehouseEntry.objects.all().count()
        context['total_transferitems'] = TransferOrderItem.objects.filter(state='EN').count()
        context['total_inprogress_orders'] = TransferOrder.objects.filter(
            state__in='IP'
        ).count()
        return context
