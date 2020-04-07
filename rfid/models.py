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

    def __str__(self):
        return self.display_name

    @property
    def total_inventory(self):
        return Item.objects.filter(sku=self).count()

    @property
    def total_locations_inventory(self):
        return Item.objects.filter(sku=self).values('current_location__id').distinct().count()


class PackingUnit(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    ACTION = (
        ('IN','Entrada'),
        ('OUT','Salida'),
        ('READ','Lectura')
    )
    epc = models.CharField(max_length=150, primary_key=True)
    current_location = models.ForeignKey(Location, null=True, on_delete=models.PROTECT, related_name="current_items")
    last_seen_location = models.ForeignKey(Location, null=True, on_delete=models.PROTECT)
    last_seen_timestamp = models.DateTimeField(null=True)
    last_seen_action = models.CharField(max_length=10, choices=ACTION, default='IN')
    display_name = models.CharField(max_length=200)
    data = HStoreField(null=True, blank=True)
    sku = models.ForeignKey(SKU, null=True, on_delete=models.PROTECT)
    in_transit = models.BooleanField(default=False)
    image = models.ImageField(null=True)
    packing_unit = models.ForeignKey(PackingUnit, null=True, blank=True, on_delete=models.PROTECT)

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
    ACTION = (
        ('IN','Entrada'),
        ('OUT','Salida'),
        ('READ','Lectura')
    )
    id = models.BigAutoField(primary_key=True)
    epc = models.CharField(max_length=150)
    node = models.ForeignKey(Node, on_delete=models.PROTECT)
    reader = models.ForeignKey(Reader, null=True, on_delete=models.PROTECT)
    antenna = models.ForeignKey(ReaderAntenna, null=True, on_delete=models.PROTECT)
    timestamp_reading = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10, choices=ACTION, default='READ')

    def __str__(self):
        return '{}-[{}]'.format(self.epc, self.reader)


class TransferOrder(models.Model):
    STATE = (
        ('RE', 'Solicitado'),
        ('IP', 'En Alistamiento'),
        ('IT', 'En Tránsito'),
        ('CO', 'Entregado')
    )
    destination = models.ForeignKey(Location, on_delete=models.PROTECT)
    expected_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=3, choices=STATE ,default='RE')

    def __str__(self):
        return '{}-[{}]'.format(self.pk, self.state)

    @property
    def total_skus(self):
        return TransferOrderItem.objects.filter(order=self).values('item__sku').distinct().count()

    @property
    def total_items(self):
        return TransferOrderItem.objects.filter(order=self).count()


class TransferOrderItem(models.Model):
    STATE = (
        ('RE',  'Por alistar'),
        ('AL',  'Alistado'),
        ('NOE', 'No entregado'),
        ('EN',  'Entregado')
    )
    order = models.ForeignKey(TransferOrder,on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    state = models.CharField(max_length=3, choices=STATE, default='RE')

    def __str__(self):
        return '{}-[{}]'.format(self.item, self.state)

    @property
    def last_out_reading(self):
        return Reading.objects.filter(epc=self.item.epc, action='OUT').order_by('-timestamp_reading').first()

    class Meta:
        unique_together = ('order', 'item')


class TransferOrderTracking(models.Model):
    order = models.ForeignKey(TransferOrder,on_delete=models.CASCADE, null=True)
    timestamp_reading = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)


class WarehouseEntry(models.Model):
    entry_date = models.DateTimeField()
    origin = models.ForeignKey(Location, on_delete=models.PROTECT)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name='warehouse_entries')

    @property
    def total_skus(self):
        return WarehouseEntryItem.objects.filter(entry=self).values('item__sku').distinct().count()

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


###Reports

class InventoryRequest(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    wait_minutes = models.PositiveIntegerField(default=10)
    init_sku = models.ForeignKey(SKU, null=True, blank=True, on_delete=models.PROTECT, related_name='inv_request_init')
    end_sku = models.ForeignKey(SKU, null=True, blank=True, on_delete=models.PROTECT, related_name='inv_request_end')
    init_location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.PROTECT, related_name='inv_request_init')
    end_location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.PROTECT, related_name='inv_request_end')
    all_locations = models.BooleanField(default=False)
    all_skus = models.BooleanField(default=False)


class InventoryReport(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    inventory_request = models.ForeignKey(InventoryRequest, on_delete=models.PROTECT, null=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.CASCADE)


class InventoryReportLine(models.Model):
    report = models.ForeignKey(InventoryReport, on_delete=models.CASCADE)
    reference = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    cant = models.IntegerField()
    packing_unit = models.CharField(max_length=200)
