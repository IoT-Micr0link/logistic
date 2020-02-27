from django.views import generic
from django_tables2 import SingleTableView
from rfid.tables import *
from statistics import mean


class InventoryView(generic.TemplateView):
    template_name = 'dashboard/logistica/inventario.html'


class ItemListView(SingleTableView):
    model = Item
    template_name = 'dashboard/logistica/inventario.html'
    table_class = ItemsTable
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['total_items'] = Item.objects.all().count()
        context['total_locations'] = Location.objects.all().count()
        context['average_age'] = mean([item.age for item in Item.objects.all()])

        return context
