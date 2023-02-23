from datetime import date, timedelta

from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models import Q


class Sites(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sites'


class Location(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=140, null=True, blank=True)
    site = models.ForeignKey(Sites, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.site.name} - {self.name}'

    class Meta:
        db_table = 'location'


class Position(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.location.name} -> {self.name}'

    class Meta:
        db_table = 'position'


class SKU(models.Model):
    display_name = models.CharField(max_length=200)
    reference_image = models.ImageField(null=True)
    datasheet = models.FileField(null=True, blank=True)
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f'<{self.pk}> {self.display_name}'

    @property
    def total_inventory(self):
        return Item.objects.filter(sku=self).count()

    @property
    def total_locations_inventory(self):
        return Item.objects.filter(sku=self).values('current_location__id').distinct().count()

    class Meta:
        db_table = 'sku'


class PackingUnit(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'packing_unit'


class Item(models.Model):
    ACTION = (
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
        ('READ', 'Lectura')
    )
    epc = models.CharField(max_length=150, primary_key=True)
    current_location = models.ForeignKey(
        Location, null=True, on_delete=models.PROTECT,
        related_name="current_items"
    )
    current_position = models.ForeignKey(Position, null=True, on_delete=models.PROTECT)
    last_seen_location = models.ForeignKey(Location, null=True, on_delete=models.PROTECT)
    last_seen_timestamp = models.DateTimeField(null=True)
    last_seen_action = models.CharField(max_length=10, choices=ACTION, default='IN')
    display_name = models.CharField(max_length=200)
    data = models.JSONField(null=True, blank=True)
    sku = models.ForeignKey(SKU, null=True, on_delete=models.PROTECT)
    in_transit = models.BooleanField(default=False)
    image = models.ImageField(null=True)
    packing_unit = models.ForeignKey(PackingUnit, null=True, blank=True, on_delete=models.PROTECT)
    origin_site = models.ForeignKey(Sites, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"<{self.epc}> {self.display_name}"

    @property
    def age(self):
        today = date.today()
        delta = today - self.last_seen_timestamp.date()
        return delta.days

    @property
    def not_seen_recently(self):
        time_threshold = timezone.now() - timedelta(seconds=settings.RFID_READING_CYCLE)
        return self.last_seen_timestamp < time_threshold

    class Meta:
        db_table = 'item'


class InventorySummary(models.Model):
    sku = models.ForeignKey(SKU, on_delete=models.DO_NOTHING)
    last_seen_location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    total_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventory_summary'
        ordering = ['sku']

    @property
    def total_missing(self):
        # missing items are those that were read in a
        # different location than expected, or that its last
        # reading was over 5 minutes ago.

        time_threshold = timezone.now() - timedelta(seconds=settings.RFID_READING_CYCLE)

        base_qs = Item.objects.filter(
            Q(last_seen_timestamp__lte=time_threshold) | ~Q(last_seen_location=self.last_seen_location),
            sku=self.sku,
            current_location=self.last_seen_location
        )

        return base_qs.count() or 0

    @property
    def total_extra(self):
        # extra items are those that were read in the current location but belong to another
        time_threshold = timezone.now() - timedelta(seconds=settings.RFID_READING_CYCLE)

        base_qs = Item.objects.filter(
            ~Q(current_location=self.last_seen_location),
            last_seen_timestamp__gte=time_threshold,
            sku=self.sku,
            last_seen_location=self.last_seen_location
        )
        return base_qs.count() or 0
