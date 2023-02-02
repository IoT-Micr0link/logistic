import django_tables2 as tables
from rfid.view_models import *
from django_tables2.utils import A


class TableBase(tables.Table):
    class Meta:
        empty_text = "No se encontraron resultados"
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        attrs = {
            "class": "table",
            "thead": {
                "class": "thead-dark"
            }
        }


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
    count = tables.Column(empty_values=(), verbose_name="Cant")
    review = tables.TemplateColumn(
        template_name="dashboard/logistics/inventory/partials/item_read_icon_cell.html",
        orderable=False, verbose_name='')

    class Meta(TableBase.Meta):
        model = Item
        sequence = (
            'serial', 'reference', 'packing','count', 'current_location', 'review'
        )
        fields = (
            'reference', 'packing', 'serial', 'count', 'current_location', 'review'
        )

    def render_count(self):
        return "1"


class ReaderTable(TableBase):
    name = tables.Column(accessor='name', verbose_name="Descripción")
    serial_number = tables.Column(accessor='serial_number', verbose_name="# Serial")
    brand = tables.Column(accessor='brand', verbose_name="Marca")

    class Meta(TableBase.Meta):
        model = Reader
        sequence = ('brand', 'name', 'serial_number')
        fields = ('brand', 'name', 'serial_number')


class ReadingsTable(TableBase):
    epc = tables.Column(accessor='epc', verbose_name="EPC")
    node = tables.Column(accessor='node.name', verbose_name="Nodo")
    reader = tables.Column(accessor='reader.name', verbose_name="Reader")
    antenna = tables.Column(accessor='antenna.name', verbose_name="Antenna")
    timestamp_reading = tables.Column(accessor='timestamp_reading', verbose_name="Timestamp")

    class Meta(TableBase.Meta):
        model = Reading
        sequence = ('timestamp_reading', 'epc', 'node', 'reader', 'antenna')
        fields = ('timestamp_reading', 'epc', 'node', 'reader', 'antenna')


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


##Tables for reports

class InventoryReportLineTable(TableBase):
    reference = tables.Column(accessor='reference', verbose_name='Referencia')
    description = tables.Column(accessor='description', verbose_name='Descripción')
    packing_unit = tables.Column(accessor='packing_unit', verbose_name='Und')

    class Meta(TableBase.Meta):
        model = InventoryReportLine
        exclude = ('id', 'report')
