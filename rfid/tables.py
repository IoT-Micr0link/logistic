import django_tables2 as tables
from rfid.view_models import *
from shared.tables import TableBase


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
