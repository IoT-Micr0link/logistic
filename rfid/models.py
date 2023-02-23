"""RFID Models"""

from django.db import models
from inventory.models import Location, Position


class Node(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=140, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    def __str__(self):
        return '{}-{}'.format(self.pk, self.location)

    class Meta:
        db_table = 'node'


class ReaderBrand(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        db_table = 'reader_brand'


class Reader(models.Model):
    name = models.CharField(max_length=140)
    serial_number = models.CharField(max_length=140, unique=True)
    brand = models.OneToOneField(ReaderBrand, on_delete=models.PROTECT)

    def __str__(self):
        return '{}-[{}]'.format(self.brand, self.serial_number)

    class Meta:
        db_table = 'reader'


class ReaderAntenna(models.Model):
    name = models.CharField(max_length=140)
    serial_number = models.CharField(max_length=140, unique=True)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    position = models.OneToOneField(
        Position, on_delete=models.DO_NOTHING, related_name='antennas',
        blank=True, null=True
    )

    def __str__(self):
        return '{}-[{}]'.format(self.name, self.name)

    class Meta:
        db_table = 'reader_antenna'


class Reading(models.Model):
    ACTION = (
        ('IN', 'Entrada'),
        ('OUT', 'Salida'),
        ('READ', 'Lectura')
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

    class Meta:
        db_table = 'reading'
