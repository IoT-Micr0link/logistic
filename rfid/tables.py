import django_tables2 as tables
from rfid.models import *
from django_tables2.utils import A


class ItemTable(tables.Table):
    epc = tables.Column(accessor='epc', verbose_name="EPC")
    display_name = tables.Column(accessor='display_name', verbose_name="Info")
    last_seen_timestamp = tables.Column(accessor='last_seen_timestamp', verbose_name="Última lectura")
    last_seen_location = tables.Column(accessor='last_seen_location', verbose_name="Ubicación lectura")

    class Meta:
        model = Item
        empty_text = "No se encontraron resultados"
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        sequence = ('epc', 'display_name', 'last_seen_timestamp', 'last_seen_location')
        fields = ('epc', 'display_name', 'last_seen_timestamp', 'last_seen_location')
        attrs = {
            "class": "table",
            "thead":{
                "class":"thead-dark"
            }
        }


class ReaderTable(tables.Table):
    name = tables.Column(accessor='name', verbose_name="Descripcion")
    serial_number = tables.Column(accessor='serial_number', verbose_name="# Serial")
    brand = tables.Column(accessor='brand', verbose_name="Marca")

    class Meta:
        model = Reader
        empty_text = "No se encontraron resultados"
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        sequence = ('brand', 'name', 'serial_number')
        fields = ('brand', 'name', 'serial_number')
        attrs = {
            "class": "table",
            "thead":{
                "class":"thead-dark"
            }
        }


class ReadingsTable(tables.Table):
    epc = tables.Column(accessor='epc', verbose_name="EPC")
    node = tables.Column(accessor='node.name', verbose_name="Nodo")
    reader = tables.Column(accessor='reader.name', verbose_name="Reader")
    antenna = tables.Column(accessor='antenna.name', verbose_name="Antenna")
    timestamp_reading = tables.Column(accessor='timestamp_reading', verbose_name="Timestamp")

    class Meta:
        model = Reading
        empty_text = "No se encontraron resultados"
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        sequence = ('timestamp_reading', 'epc', 'node', 'reader', 'antenna')
        fields = ('timestamp_reading', 'epc', 'node', 'reader', 'antenna')
        attrs = {
            "class": "table",
            "thead":{
                "class":"thead-dark"
            }
        }


class TransferOrderTable(tables.Table):
    id = tables.Column(accessor='id', verbose_name="ID")
    destination = tables.Column(accessor='destination', verbose_name="Destino")
    expected_completion_date = tables.Column(accessor='expected_completion_date', verbose_name="Fecha esperada de entrega")
    actual_completion_date = tables.Column(accessor='actual_completion_date', verbose_name="Fecha real de entrega ")
    state = tables.Column(accessor='state', verbose_name="Estado")
    detalle = tables.LinkColumn('logistica-transfer-order-detail', text="ver detalle",
                                       args=[A('id')])

    class Meta:
        model = Reading
        empty_text = "No se encontraron resultados"
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        sequence = ('id', 'destination', 'expected_completion_date', 'actual_completion_date', 'state')
        fields = ('id', 'destination', 'expected_completion_date', 'actual_completion_date', 'state')
        attrs = {
            "class": "table",
            "thead":{
                "class":"thead-dark"
            }
        }


class TransferOrderItemTable(tables.Table):
    epc = tables.Column(accessor='item.epc', verbose_name="EPC")
    item = tables.Column(accessor='item.display_name', verbose_name="Item")
    state = tables.Column(accessor='state', verbose_name="Estado")

    class Meta:
        model = Reading
        empty_text = "No se encontraron resultados"
        template_name = 'django_tables2/bootstrap4.html'
        orderable = False
        sequence = ('epc', 'item', 'state', )
        fields = ('epc', 'item', 'state', )
        attrs = {
            "class": "table",
            "thead":{
                "class":"thead-dark"
            }
        }