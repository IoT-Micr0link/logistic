from django.core.management import BaseCommand

from rfid.models import Reading
from warehouse.models import TransferOrderItem, TransferOrder, WarehouseEntryItem, WarehouseEntry


class Command(BaseCommand):

    help = 'Deletes records from specified models.'

    def handle(self, *args, **options):
        Reading.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all records from Readings.'))

        TransferOrderItem.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all records from TransferOrderItem.'))

        TransferOrder.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all records from TransferOrder.'))

        WarehouseEntryItem.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all records from WarehouseEntryItem.'))

        WarehouseEntry.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all records from WarehouseEntry.'))