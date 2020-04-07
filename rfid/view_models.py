from django.db import models
from rfid.models import *

# These models are intended for database views


class InventorySummary(models.Model):
    sku = models.ForeignKey(SKU, on_delete=models.DO_NOTHING)
    current_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    packing_unit = models.ForeignKey(PackingUnit, on_delete=models.DO_NOTHING)
    total_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventory_summary'
        ordering = ['sku']

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return


class LastReadingsSnapshot(models.Model):
    epc = models.CharField(max_length=150, primary_key=True)
    timestamp_reading = models.DateTimeField()
    antenna = models.ForeignKey(ReaderAntenna, null=True, on_delete=models.DO_NOTHING)
    reader = models.ForeignKey(Reader, null=True, on_delete=models.DO_NOTHING)
    node = models.ForeignKey(Node, null=True, on_delete=models.DO_NOTHING)
    sku = models.ForeignKey(SKU, null=True, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(Location, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'last_readings_snapshot'

    def save(self, *args, **kwargs):
        return

    def delete(self, *args, **kwargs):
        return

