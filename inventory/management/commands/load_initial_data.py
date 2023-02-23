import csv
import os
from datetime import datetime

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from inventory import models

FILES = {
    'skus': 'data/skus.csv',
    'items': 'data/items.csv'
}
CSV_DELIMITER = os.getenv('CSV_DELIMITER', ',')


class Command(BaseCommand):

    def handle(self, *args, **options):
        for name, path in FILES.items():
            self.load_info(filename=name, file_path=path)
            self.stdout.write(
                self.style.SUCCESS(f'successfully elements added on {name} table')
            )

    @transaction.atomic
    def load_info(self, filename: str, file_path: str) -> None:
        function = getattr(self, f'load_{filename}')
        function(file_path)

    def load_skus(self, file_path: str):
        skus = []
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file, delimiter=CSV_DELIMITER)
            for row in reader:
                if models.SKU.objects.filter(display_name=row.get('display_name')).exists():
                    continue

                data = self._extract_data(row)
                image = File(
                    open(os.path.join(settings.BASE_DIR, 'images', row.get('reference_image')), 'rb'),
                    f'image_{row.get("reference_image")}'
                )
                datasheet = File(
                    open(os.path.join(settings.BASE_DIR, 'datasheets', row.get('datasheet')), 'rb'),
                    f'datasheet_{row.get("display_name")}'
                )
                _sku = models.SKU(
                    display_name=row.get('display_name'),
                    reference_image=image,
                    datasheet=datasheet,
                    data=data
                )
                skus.append(_sku)
            models.SKU.objects.bulk_create(skus)

    def load_items(self, file_path: str):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file, delimiter=',')
            items = []
            for row in reader:
                if models.Item.objects.filter(epc=row.get('epc')).exists():
                    continue

                image = File(
                    open(os.path.join(settings.BASE_DIR, 'images', row.get('image')), 'rb'),
                    f'image_{row.get("image")}'
                )
                data = self._extract_data(row)
                _item = models.Item(
                    epc=row.get('epc'),
                    display_name=row.get('display_name'),
                    last_seen_action=row.get('last_seen_action', ''),
                    packing_unit_id=row.get(
                        'packing_unit', models.PackingUnit.objects.first().id
                    ),
                    origin_site_id=row.get('origin_site', models.Sites.objects.first().id),
                    last_seen_timestamp=datetime.now().date(),
                    last_seen_location_id=row.get('last_seen_location_id'),
                    current_location_id=row.get(
                        'current_location', models.Location.objects.first().id
                    ),
                    data=data,
                    image=image,
                    sku_id=row.get('sku_id'),
                )
                items.append(_item)
            models.Item.objects.bulk_create(items)

    @staticmethod
    def _extract_data(row: dict):
        _data = {
            key.split('.')[1]: row.get(key)
            for key in
            filter(lambda key: key.startswith('data.'), row.keys())
        }
        return _data or {}
