import csv
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from rfid import models

FILES = {
    'items': 'data/items.csv',
    'skus': 'data/clean_skus.csv'
}


class Command(BaseCommand):

    help = 'table\'s name to load initial info, must correspond '
    'to a file in data folder'

    def add_arguments(self, parser):
        parser.add_argument(
            '--tables', '-t', nargs='+', type=str,
        )

    def handle(self, *args, **options):
        filenames = options.get('tables')
        for filename in filenames:
            file = FILES.get(filename)
            if not file:
                raise CommandError('there is no file with that table name')
            self.load_info(filename=filename, file_path=file)
            self.stdout.write(self.style.SUCCESS(f'successfully {filename} elements added'))

    @transaction.atomic
    def load_info(self, filename: str, file_path: str) -> None:
        function = getattr(self, f'load_{filename}')
        function(file_path)

    def load_skus(self, file_path: str):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file, delimiter=';')
            skus = []
            for row in reader:
                _sku = models.SKU(
                    display_name=row.get('ni_name'),
                    data={
                        'description': row.get('ni_descripcion')
                    }
                )
                skus.append(_sku)
            models.SKU.objects.bulk_create(skus)

    def load_items(self, file_path: str):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file, delimiter=',')
            items = []
            for row in reader:
                _item = models.Item(
                    sku_id=row.get('idlog_inv_unidades'),
                    epc=row.get('codigo_sap'),
                    display_name=row.get('ni_name'),
                    last_seen_action='IN',
                    packing_unit=models.PackingUnit.objects.first(),
                    origin_site=models.Sites.objects.first(),
                    last_seen_timestamp=datetime.now().date(),
                    current_location=models.Location.objects.first(),
                )
                items.append(_item)
            models.Item.objects.bulk_create(items)
