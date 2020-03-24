import django_tables2 as tables
from rfid.models import *
from django_tables2.utils import A


class TableBase(tables.Table):
    class Meta:
        empty_text = "No se encontraron resultados"
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        attrs = {
            "class": "table",
            "thead":{
                "class":"thead-dark"
            }
        }


class SkuInventoryTable(TableBase):
    display_name = tables.Column(accessor='display_name', verbose_name="Descripción")
    total_inventory = tables.Column(accessor='total_inventory', verbose_name="Total inventario")
    total_locations_inventory = tables.Column(accessor='total_locations_inventory', verbose_name="En cuantas bodegas")
    detail = tables.LinkColumn('logistics-sku-detail', text="ver detalle", verbose_name="Ver detalle",
                                       args=[A('id')])


    class Meta(TableBase.Meta):
        model = SKU
        fields = ('id', 'display_name', 'total_inventory','total_locations_inventory', 'detail')



class ItemTable(TableBase):
    epc = tables.Column(accessor='epc', verbose_name="EPC")
    display_name = tables.Column(accessor='display_name', verbose_name="Referencia")
    last_seen_timestamp = tables.Column(accessor='last_seen_timestamp', verbose_name="Última lectura")
    last_seen_location = tables.Column(accessor='last_seen_location', verbose_name="Bodega lectura")
    last_seen_action = tables.Column(accessor='last_seen_action', verbose_name="Tipo de accion")
    #in_transit = tables.TemplateColumn(template_name="dashboard/logistics/inventory/partials/in_transit_cell.html",
    #                                        orderable=False)


    class Meta(TableBase.Meta):
        model = Item
        sequence = ('epc', 'display_name', 'last_seen_timestamp', 'last_seen_location', 'last_seen_action')
        fields = ('epc', 'display_name', 'last_seen_timestamp', 'last_seen_location', 'last_seen_action')


class ReaderTable(TableBase):
    name = tables.Column(accessor='name', verbose_name="Descripcion")
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
    id = tables.Column(accessor='id', verbose_name="ID")
    destination = tables.Column(accessor='destination', verbose_name="Destino")
    expected_completion_date = tables.Column(accessor='expected_completion_date', verbose_name="Fecha esperada de entrega")
    actual_completion_date = tables.Column(accessor='actual_completion_date', verbose_name="Fecha real de entrega ")
    state = tables.Column(accessor='state', verbose_name="Estado")
    detalle = tables.LinkColumn('logistics-transfer-order-detail', text="ver detalle",
                                       args=[A('id')])

    class Meta(TableBase.Meta):
        model = TransferOrder
        sequence = ('id', 'destination', 'expected_completion_date', 'actual_completion_date', 'state')
        fields = ('id', 'destination', 'expected_completion_date', 'actual_completion_date', 'state')


class TransferOrderItemTable(TableBase):
    sku = tables.Column(accessor='item.sku.display_name', verbose_name="Referencia")
    epc = tables.Column(accessor='item.epc', verbose_name="Serial")
    count = tables.Column(empty_values=(), verbose_name="Cant")
    state = tables.Column(accessor='state', verbose_name="Estado")

    class Meta(TableBase.Meta):
        model = TransferOrderItem
        sequence = ('sku', 'epc', 'state', )
        fields = ('sku', 'epc', 'state', )

    def render_count(self):
        return "1"


class WarehouseEntryTable(TableBase):
    id = tables.Column(accessor='id', verbose_name="ID")
    origin = tables.Column(accessor='origin', verbose_name="Origen")
    location = tables.Column(accessor='location', verbose_name="Bodega de recepción")
    entry_date = tables.Column(accessor='entry_date', verbose_name="Fecha de recepción")
    total_items = tables.Column(accessor='total_items', verbose_name="Total Items")

    detail = tables.LinkColumn('logistics-warehouse-entry-detail', text="ver detalle",
                                       args=[A('id')])

    class Meta(TableBase.Meta):
        model = WarehouseEntry
        sequence = ('id', 'origin', 'location', 'entry_date', 'total_items', 'detail')
        fields = ('id', 'origin', 'location', 'entry_date', 'total_items', 'detail')


class WarehouseEntryItemTable(TableBase):
    sku = tables.Column(accessor='item.sku.display_name', verbose_name="Referencia")
    epc = tables.Column(accessor='item.epc', verbose_name="Serial")
    count = tables.Column(empty_values=(), verbose_name="Cant")
    detail = tables.LinkColumn('logistics-sku-detail', text="ver detalle", verbose_name="Ver detalle",
                                       args=[A('item__sku_id')])

    class Meta(TableBase.Meta):
        model = WarehouseEntryItem
        sequence = ('sku','epc','count','detail')
        fields = ('sku','epc','count','detail')

    def render_count(self):
        return "1"