# These models are intended for database views
from inventory.models import SKU
from rfid.models import *


class LastReadingsSnapshot(models.Model):
    epc = models.CharField(max_length=150, primary_key=True)
    timestamp_reading = models.DateTimeField()
    antenna = models.ForeignKey(ReaderAntenna, null=True, on_delete=models.DO_NOTHING)
    reader = models.ForeignKey(Reader, null=True, on_delete=models.DO_NOTHING)
    node = models.ForeignKey(Node, null=True, on_delete=models.DO_NOTHING)
    sku = models.ForeignKey(SKU, null=True, on_delete=models.DO_NOTHING)
    location = models.ForeignKey(Location, null=True, on_delete=models.DO_NOTHING)
    position = models.ForeignKey(Position, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'last_readings_snapshot'
