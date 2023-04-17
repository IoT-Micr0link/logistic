import argparse
import csv
import os

from django.core.management import BaseCommand
from django.db import transaction

from inventory.models import PackingUnit, Sites, Location, Position
from rfid.models import ReaderBrand, Reader, ReaderAntenna, Node


class Command(BaseCommand):
    detail = 'Loads the initial data for rfid module'

    def add_arguments(self, parser):
        parser.add_argument('--from_files', '-f', action=argparse.BooleanOptionalAction)

    def handle(self, *args, **options):
        if options.get('from_files'):
            self.from_files()
        else:
            PackingUnit.objects.create(
                name='Und',
                description='Unidades'
            )
            self.create_logistic_entities()
            self.create_rfid_entities()
        self.stdout.write(self.style.SUCCESS('Project set up successfully'))

    @transaction.atomic
    def create_logistic_entities(self):
        site = Sites.objects.create(name=os.getenv('SITE_NAME', 'Microlink'))
        location_1 = Location.objects.create(
            name='Bodega 7',
            description='Bodega 7',
            site=site
        )
        Location.objects.create(name='Bodega 8', description='Bodega 8', site=site)
        Position.objects.create(name='E-3-2-D', location=location_1)
        Position.objects.create(name='E-5-2-D', location=location_1)

    @transaction.atomic
    def create_rfid_entities(self):
        reader_brand = ReaderBrand.objects.create(name='Zebra')
        reader = Reader.objects.create(
            name='FX9600', serial_number='20026010550819',
            brand=reader_brand
        )
        ReaderAntenna.objects.create(
            name='Read', serial_number=3,
            reader=reader,
            position=Position.objects.filter(name='E-5-2-D').first()
        )
        ReaderAntenna.objects.create(
            name='Out', serial_number=2, reader=reader,
        )
        ReaderAntenna.objects.create(
            name='Read', serial_number=1,
            reader=reader,
            position=Position.objects.filter(name='E-3-2-D').first()
        )
        Node.objects.create(
            name='Kerlink', description='Kerlink Inventory',
            location=Location.objects.filter(name='Bodega 7').first()
        )

    def from_files(self):
        path = 'info'
        entities = ['sites', 'packing_units', 'locations', 'positions', 'ReaderBrands', 'Reader']
        for entity in entities:
            file_path = os.path.join(path, f'{entity}.csv')
            with open(file_path, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entity_object = globals()[entity.title()]()
                    for key, value in row.items():
                        setattr(entity_object, key, value)
                    entity_object.save()