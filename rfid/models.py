from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)


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

    def __str__(self):
        return '{}-[{}]'.format(self.epc, self.reader)
