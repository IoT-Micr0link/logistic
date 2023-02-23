from django.db import models

from inventory.models import Location, Item
from rfid.models import Reading


class TransferOrder(models.Model):
    STATE = (
        ('RE', 'Solicitado'),
        ('IP', 'En Alistamiento'),
        ('IT', 'En Tránsito'),
        ('CO', 'Entregado')
    )
    destination = models.ForeignKey(Location, on_delete=models.PROTECT)
    expected_completion_date = models.DateField()
    actual_completion_date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(max_length=3, choices=STATE, default='RE')

    def __str__(self):
        return '{}-[{}]'.format(self.pk, self.state)

    @property
    def total_skus(self):
        return TransferOrderItem.objects.filter(order=self).values('item__sku').distinct().count()

    @property
    def total_items(self):
        return TransferOrderItem.objects.filter(order=self).count()

    class Meta:
        db_table = 'transfer_order'


class TransferOrderItem(models.Model):
    STATE = (
        ('RE', 'Por alistar'),
        ('AL', 'Alistado'),
        ('NOE', 'No entregado'),
        ('EN', 'Entregado')
    )
    order: TransferOrder = models.ForeignKey(
        TransferOrder, on_delete=models.CASCADE, null=True
    )
    item: Item = models.OneToOneField(Item, on_delete=models.PROTECT)
    state = models.CharField(max_length=3, choices=STATE, default='RE')

    def __str__(self):
        return '{}-{}-[{}]'.format(self.item.display_name, self.item.epc, self.state)

    @property
    def last_out_reading(self):
        return Reading.objects.filter(
            epc=self.item.epc,
            action='OUT'
        ).order_by('-timestamp_reading').first()

    class Meta:
        db_table = 'transfer_order_item'
        unique_together = ('order', 'item')


class TransferOrderTracking(models.Model):
    order = models.ForeignKey(TransferOrder, on_delete=models.CASCADE, null=True)
    timestamp_reading = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        db_table = 'transfer_order_tracking'


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

    class Meta:
        db_table = 'warehouse_entry'


class WarehouseEntryItem(models.Model):
    entry = models.ForeignKey(WarehouseEntry, on_delete=models.PROTECT)
    item: Item = models.ForeignKey(Item, on_delete=models.PROTECT)

    def __str__(self):
        return '{}-[{}]'.format(self.entry, self.item.epc)

    class Meta:
        db_table = 'warehouse_entry_item'
        unique_together = ('entry', 'item')
