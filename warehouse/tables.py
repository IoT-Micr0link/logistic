import django_tables2 as tables
from django_tables2 import A

from shared.tables import TableBase
from warehouse.models import TransferOrder, TransferOrderItem, WarehouseEntry, WarehouseEntryItem


class TransferOrderTable(TableBase):
    id = tables.Column(accessor='id', verbose_name="Número pedido ")
    destination = tables.Column(accessor='destination', verbose_name="Destino")
    actual_completion_date = tables.Column(accessor='actual_completion_date', verbose_name="Fecha de entrega ")
    state = tables.Column(accessor='state', verbose_name="Estado")
    total_items = tables.Column(accessor='total_items', verbose_name="Total Items")
    detalle = tables.LinkColumn('logistics:transfer-order-detail', text="ver detalle",
                                args=[A('id')])

    class Meta(TableBase.Meta):
        model = TransferOrder
        sequence = ('id', 'destination', 'actual_completion_date', 'state', 'total_items')
        fields = ('id', 'destination', 'actual_completion_date', 'state', 'total_items')


class TransferOrderItemTable(TableBase):
    reference = tables.Column(accessor='item.sku.display_name', verbose_name="Referencia")
    description = tables.TemplateColumn(
        template_name="dashboard/logistics/inventory/partials/item_description_cell.html"
        , verbose_name="Descripción")
    epc = tables.Column(accessor="item.epc", verbose_name="Serial")
    count = tables.Column(empty_values=(), verbose_name="Cant")
    state = tables.Column(accessor="state", verbose_name="Estado")
    packing_unit = tables.Column(accessor="item.packing_unit", verbose_name="Unidad")
    fecha_ultimo_registro = tables.Column(accessor="last_out_reading.timestamp_reading",
                                          verbose_name="Fecha lectura")

    class Meta(TableBase.Meta):
        model = TransferOrderItem
        sequence = ('reference', 'description', 'epc', 'state', 'count', 'packing_unit', 'fecha_ultimo_registro')
        fields = ('reference', 'description', 'epc', 'state', 'count', 'packing_unit', 'fecha_ultimo_registro')

    def render_count(self):
        return "1"


class WarehouseEntryTable(TableBase):
    id = tables.Column(accessor="id", verbose_name="Id entrada")
    origin = tables.Column(accessor="origin", verbose_name="Origen")
    location = tables.Column(accessor="location", verbose_name="Bodega de recepción")
    entry_date = tables.Column(accessor="entry_date", verbose_name="Fecha de recepción")
    total_items = tables.Column(accessor="total_items", verbose_name="Total Items")

    detail = tables.LinkColumn("logistics:warehouse-entry-detail", text="ver detalle", verbose_name="Ver detalle",
                               args=[A('id')])

    class Meta(TableBase.Meta):
        model = WarehouseEntry
        sequence = ('id', 'origin', 'location', 'entry_date', 'total_items', 'detail')
        fields = ('id', 'origin', 'location', 'entry_date', 'total_items', 'detail')


class WarehouseEntryItemTable(TableBase):
    reference = tables.Column(accessor='item.sku.display_name', verbose_name="Referencia")
    description = tables.TemplateColumn(
        template_name="dashboard/logistics/inventory/partials/item_description_cell.html"
        , verbose_name="Descripción")
    epc = tables.Column(accessor='item.epc', verbose_name="Serial")
    count = tables.Column(empty_values=(), verbose_name="Cant")
    packing_unit = tables.Column(accessor='item.packing_unit', verbose_name="Unidad")

    class Meta(TableBase.Meta):
        model = WarehouseEntryItem
        sequence = ('reference', 'description', 'epc', 'count', 'packing_unit')
        fields = ('reference', 'description', 'epc', 'count', 'packing_unit')

    def render_count(self):
        return "1"
