import django_tables2 as tables
from rfid.models import *


class ItemsTable(tables.Table):
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

