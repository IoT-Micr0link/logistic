from datetime import datetime, timedelta

from django.conf import settings
from django_tables2 import SingleTableView

from inventory.models import Item
from rfid.tables import *
from django.db.models import OuterRef, Exists


class ReadingsListView(SingleTableView):
    model = Reading
    template_name = 'dashboard/rfid/readings_list.html'
    table_class = ReadingsTable
    table_pagination = {
        'per_page': 30
    }

    def get_queryset(self):
        return Reading.objects.annotate(
            exists=Exists(
                Item.objects.filter(epc=OuterRef('epc'))
            )
        ).exclude(exists=False).filter(
            timestamp_reading__gte=(
                datetime.now() - timedelta(minutes=settings.RFID_READING_CYCLE)
            )
        )

    def get_context_data(self, **kwargs):
        context = super(ReadingsListView, self).get_context_data(**kwargs)
        context['items_count'] = self.get_queryset().distinct('epc').count()
        context['location'] = Location.objects.first()
        context['reader'] = Reader.objects.first()
        context['timestamp'] = datetime.now().isoformat()
        return context


class ReadersListView(SingleTableView):
    model = Reader
    template_name = 'dashboard/rfid/readers_list.html'
    table_class = ReaderTable
    table_pagination = {
        'per_page': 30
    }

    def get_context_data(self, **kwargs):
        context = super(ReadersListView, self).get_context_data(**kwargs)
        context['total_nodes'] = Node.objects.all().count()
        context['total_readers'] = Reader.objects.all().count()
        context['total_antennas'] = ReaderAntenna.objects.all().count()

        return context
