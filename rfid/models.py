from django.db import models
from datetime import date
from django.contrib.postgres.fields import HStoreField


class Location(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class SKU(models.Model):
    display_name = models.CharField(max_length=200)
    reference_image = models.ImageField(null=True)
    datasheet = models.FileField(null=True, blank=True)
    data = HStoreField(null=True, blank=True)

    @property
    def total_inventory(self):
        return Item.objects.filter(sku=self).count()


class Item(models.Model):
    epc = models.CharField(max_length=48, primary_key=True)
    last_seen_location = models.ForeignKey(Location, null=True, on_delete=models.PROTECT)
    last_seen_timestamp = models.DateTimeField(null=True)
    display_name = models.CharField(max_length=200)
    data = HStoreField(null=True, blank=True)
    sku = models.ForeignKey(SKU, null=True, on_delete=models.PROTECT)
    in_transit = models.BooleanField(default=False)
    image = models.ImageField(null=True)

    @property
    def age(self):
        today = date.today()
        delta = today - self.last_seen_timestamp.date()
        return delta.days


class Node(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=140, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return '{}-{}'.format(self.id, self.location)


class ReaderBrand(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return '{}'.format(self.name)


class Reader(models.Model):
    name = models.CharField(max_length=140)
    serial_number = models.CharField(max_length=140, unique=True)
    brand = models.ForeignKey(ReaderBrand, on_delete=models.PROTECT)

    def __str__(self):
        return '{}-[{}]'.format(self.brand, self.serial_number)


class ReaderAntenna(models.Model):
    name = models.CharField(max_length=140)
    serial_number = models.CharField(max_length=140, unique=True)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-[{}]'.format(self.name, self.name)


class Reading(models.Model):
    id = models.BigAutoField(primary_key=True)
    epc = models.CharField(max_length=24)
    node = models.ForeignKey(Node, on_delete=models.PROTECT)
    reader = models.ForeignKey(Reader, null=True, on_delete=models.PROTECT)
    antenna = models.ForeignKey(ReaderAntenna, null=True, on_delete=models.PROTECT)
    timestamp_reading = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-[{}]'.format(self.epc, self.reader)


class TransferOrder(models.Model):
    STATE = (
        ('RE', 'Solicitado'),
        ('IP', 'En progreso'),
        ('CO', 'Completado')
    )
    destination = models.ForeignKey(Location, on_delete=models.PROTECT)
    expected_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=3, choices=STATE ,default='RE')

    def __str__(self):
        return '{}-[{}]'.format(self.pk, self.state)


class TransferOrderItem(models.Model):
    STATE = (
        ('RE',  'Solicitado'),
        ('AL',  'Alistado'),
        ('NOE', 'No entregado'),
        ('EN',  'Entregado')
    )
    order = models.ForeignKey(TransferOrder,on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    state = models.CharField(max_length=3, choices=STATE, default='RE')

    def __str__(self):
        return '{}-[{}]'.format(self.item, self.state)

    class Meta:
        unique_together = ('order', 'item')


class WarehouseEntry(models.Model):
    entry_date = models.DateTimeField()
    origin = models.ForeignKey(Location, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='warehouse_entries')

    @property
    def total_items(self):
        return WarehouseEntryItem.objects.filter(entry=self).count()

    def __str__(self):
        return '{}-[{}]'.format(self.pk, self.origin)


class WarehouseEntryItem(models.Model):
    entry = models.ForeignKey(WarehouseEntry,on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)

    def __str__(self):
        return '{}-[{}]'.format(self.entry, self.item.epc)

    class Meta:
        unique_together = ('entry', 'item')





