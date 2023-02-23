from dal import autocomplete
from django.db.models import Count, F
from django.views.generic import DetailView
from django_tables2 import SingleTableView, SingleTableMixin

from inventory.filters import SKUFilter, ItemFilter, InventorySummaryFilter, ItemListFilter
from inventory.forms import SKUfilterForm, InventorySummaryFilterForm, ItemFilterForm
from inventory.models import SKU, Location, Item, InventorySummary
from inventory.tables import SkuInventoryTable, SKUDetailTable, ItemTable, InventorySummaryTable


class SKUInventoryView(SingleTableView):
    model = SKU
    template_name = 'dashboard/logistics/inventory/inventory_by_sku.html'
    table_class = SkuInventoryTable
    filterset_class = SKUFilter
    filterset_form = SKUfilterForm
    table_pagination = {
        'per_page': 30
    }

    def get_table_data(self):
        return self.filterset_class(self.request.GET, queryset=SKU.objects.all()).qs

    def get_context_data(self, **kwargs):
        context = super(SKUInventoryView, self).get_context_data(**kwargs)
        form = self.filterset_form(self.request.GET or None)
        filter = self.filterset_class(self.request.GET, queryset=SKU.objects.all())
        context["form"] = form
        context["filter"] = filter
        return context


class SKUDetailView(SingleTableMixin, DetailView):
    model = SKU
    template_name = 'dashboard/logistics/inventory/sku_detail.html'
    table_class = SKUDetailTable
    filterset_class = ItemFilter
    table_pagination = {
        'per_page': 5
    }

    def get_table_class(self):
        if not self.request.GET.get('current_location'):
            return SKUDetailTable
        else:
            return ItemTable

    def get_table_data(self):
        if not self.request.GET.get('current_location'):
            return Item.objects.filter(sku=self.object.id) \
                .values('current_location_id', 'current_location__description',
                        'sku_id', 'sku__display_name') \
                .annotate(sku_description=F('sku__display_name'),
                          location_id=F('current_location_id'),
                          location=F('current_location__name'),
                          total=Count('current_location_id',
                                      distinct=False)).order_by('-total')
        else:
            return self.filterset_class(self.request.GET,
                                        queryset=Item.objects.filter(sku=self.object.id)).qs

    def get_context_data(self, **kwargs):
        context = super(SKUDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('current_location'):
            context['filter'] = (
                self.filterset_class(self.request.GET, queryset=Item.objects.filter(
                    sku=self.object.id))
            )
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


class ItemListView(SingleTableView):
    model = Item
    template_name = 'dashboard/logistics/inventory/inventory_by_item.html'
    table_class = ItemTable
    filterset_class = ItemListFilter
    filterset_form = ItemFilterForm
    table_pagination = {
        'per_page': 30
    }

    def get_table_data(self):
        return self.filterset_class(self.request.GET, queryset=Item.objects.all()).qs

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context['total_locations'] = Location.objects.all().count()
        context['form'] = self.filterset_form(self.request.GET or None)
        context['filter'] = self.filterset_class(
            self.filterset_class(self.request.GET, queryset=Item.objects.all())
        )
        context['total_locations_in_use'] = \
            Item.objects.all().values('current_location__id').distinct().count()
        return context


class ItemDetailView(SingleTableMixin, DetailView):
    model = Item
    template_name = 'dashboard/logistics/inventory/item-detail.html'
    context_object_name = "sku_object"
    table_class = ItemTable
    filterset_class = ItemFilter
    table_pagination = {
        'per_page': 10
    }

    def get_table_data(self):
        return self.filterset_class(
            self.request.GET,
            queryset=Item.objects.filter(
                sku=self.object.sku
            ).exclude(epc=self.object.epc)
        ).qs

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        filter = self.filterset_class(self.request.GET, queryset=Item.objects.filter(sku=self.object.sku))
        context['location_id'] = self.request.GET.get('current_location')
        context['filter'] = filter
        context['locations_inventory_list'] = Item.objects.filter(sku=self.object.sku) \
            .exclude(epc=self.object.epc) \
            .values('current_location_id', 'current_location__name') \
            .annotate(total=Count('current_location_id')).order_by('-total')
        return context


# Autocompletes

# Autocompletes
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


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Item.objects.all()
        if self.q:
            qs = qs.filter(display_name__istartswith=self.q)
        return qs
