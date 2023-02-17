from django.db import models

from inventory.models import SKU, Location


class InventoryRequest(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(null=True, blank=True)
    wait_minutes = models.PositiveIntegerField(default=10)
    init_sku = models.ForeignKey(SKU, null=True, blank=True, on_delete=models.PROTECT,
                                 related_name='inv_request_init')
    end_sku = models.ForeignKey(SKU, null=True, blank=True, on_delete=models.PROTECT,
                                related_name='inv_request_end')
    init_location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.PROTECT,
                                      related_name='inv_request_init')
    end_location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.PROTECT,
                                     related_name='inv_request_end')
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