# These models are intended for database views
from rfid.models import *
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


class InventorySummary(models.Model):
    epc = models.IntegerField()
    sku = models.ForeignKey(SKU, on_delete=models.DO_NOTHING)
    current_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    packing_unit = models.ForeignKey(PackingUnit, on_delete=models.DO_NOTHING)
    total_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventory_summary'
        ordering = ['epc']

    @property
    def total_missing(self):
        # missing items are those that were read in a
        # different location than expected, or that its last
        # reading was over 5 minutes ago.

        time_threshold = timezone.now() - timedelta(minutes=settings.RFID_READING_CYCLE)

        base_qs = Item.objects.filter(
            Q(last_seen_timestamp__lte=time_threshold) | ~Q(last_seen_location=self.current_location),
            sku=self.sku,
            #packing_unit=self.packing_unit,
            current_location=self.current_location
        )

        return base_qs.count() or 0

    @property
    def total_extra(self):
        # extra items are those that were read in the current location but belong to another
        time_threshold = timezone.now() - timedelta(minutes=settings.RFID_READING_CYCLE)

        base_qs = Item.objects.filter(
            ~Q(current_location=self.current_location),
            last_seen_timestamp__gte=time_threshold,
            sku=self.sku,
            #packing_unit=self.packing_unit,
            last_seen_location=self.current_location
        )
        return base_qs.count() or 0

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
