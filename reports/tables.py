##Tables for reports
from django_tables2 import tables

from reports.models import InventoryReportLine
from shared.tables import TableBase


class InventoryReportLineTable(TableBase):
    reference = tables.Column(accessor='reference', verbose_name='Referencia')
    description = tables.Column(accessor='description', verbose_name='Descripción')
    packing_unit = tables.Column(accessor='packing_unit', verbose_name='Und')

    class Meta(TableBase.Meta):
        model = InventoryReportLine
        exclude = ('id', 'report')