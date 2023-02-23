import time
import random

import requests
from django.conf import settings
from django.core.management import BaseCommand

from inventory.models import Item


class Command(BaseCommand):

    help = 'Instantiate a little example of how rfid hardware ' \
           'catch up data'

    def handle(self, *args, **options):
        print('RFID simulation started...')
        print('Elements to simulate are:')
        for item in Item.objects.all():
            print(item.epc)
        print('-' * 50)
        try:
            while True:
                events = generate_data()
                requests.post('http://localhost:8000/api/readings/zebra/', json=events)
                time.sleep(settings.RFID_READING_CYCLE)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Simulation ended'))


def generate_data():
    read_antennas = [1, 3]
    items = Item.objects.all()
    events = []

    for item in items:
        antenna = random.choice(read_antennas)
        events.append(
            {
                'data': {
                    'idHex': item.epc,
                    'antenna': antenna
                }
            }
        )
        print(f'epc: {item.epc} on antenna {antenna}')
    print('-' * 50)
    return events
