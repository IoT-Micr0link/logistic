import django_tables2 as tables

from inventory.models import SKU, InventorySummary, Item
from shared.tables import TableBase


class SkuInventoryTable(TableBase):
    display_name = tables.Column(accessor='display_name', verbose_name="Descripción")
    total_inventory = tables.Column(accessor='total_inventory', verbose_name="Total Inventario",
                                    order_by='total_inventory')
    total_locations_inventory = tables.Column(accessor='total_locations_inventory', verbose_name="Por Bodegas")
    review = tables.TemplateColumn(
        template_name='dashboard/logistics/inventory/partials/reference_detail.html',
        verbose_name='Detalle'
    )

    class Meta(TableBase.Meta):
        model = SKU
        fields = ('id', 'display_name', 'total_inventory', 'total_locations_inventory', 'review')


class InventorySummaryTable(TableBase):
    reference = tables.TemplateColumn(
        verbose_name='Referencia',
        template_name="dashboard/logistics/inventory/partials/item_reference_cell.html"
    )
    display_name = tables.Column(verbose_name='Nombre', accessor='sku.display_name')
    last_seen_location = tables.Column(accessor='last_seen_location.name', verbose_name="Bodega")
    total_count = tables.Column(accessor='total_count', verbose_name="Total Inventario")
    review = tables.TemplateColumn(
        template_name='dashboard/logistics/inventory/partials/item_inventory_count_cell.html',
        verbose_name='Revisar'
    )

    class Meta(TableBase.Meta):
        model = InventorySummary
        order_by = 'reference'
        fields = ('reference', 'display_name', 'last_seen_location', 'total_count', 'review')


class SKUDetailTable(TableBase):
    id = tables.Column(accessor='sku_id', verbose_name='ID')
    display_name = tables.Column(accessor='sku_description', verbose_name='Referencia')
    location_description = tables.Column(accessor='location', verbose_name='Bodega')
    total = tables.Column(accessor='total', verbose_name='Total Unidades')
    detail = tables.TemplateColumn(
        template_name='dashboard/logistics/inventory/partials/sku_detail.html',
        verbose_name='Detalle'
    )

    class Meta(TableBase.Meta):
         model = SKU
         sequence = ('id', 'display_name', 'location_description', 'total')
         fields = ('id', 'display_name', 'detail', 'total', 'location_description')


class ItemTable(TableBase):
    serial = tables.TemplateColumn(
        verbose_name="EPC",
        template_name="dashboard/logistics/inventory/partials/item_reference_cell.html",)
    reference = tables.Column(accessor='display_name', verbose_name='Referencia')
    packing = tables.Column(accessor='packing_unit__name', verbose_name='Packing')
    current_location = tables.Column(accessor='current_location', verbose_name="Bodega")
    current_position = tables.Column(accessor='current_position', verbose_name='Posicion')
    review = tables.TemplateColumn(
        template_name="dashboard/logistics/inventory/partials/item_read_icon_cell.html",
        orderable=False, verbose_name='')

    class Meta(TableBase.Meta):
        model = Item
        sequence = (
            'serial', 'reference', 'packing', 'current_location', 'current_position', 'review'
        )
        fields = (
            'reference', 'packing', 'serial', 'current_location', 'current_position', 'review'
        )
