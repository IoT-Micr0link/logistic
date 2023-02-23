from datetime import datetime, timedelta

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from inventory.models import Item
from rfid.view_models import *
from django.db.models import Count, Q

from rest_framework.decorators import api_view

from warehouse.models import TransferOrderTracking, TransferOrderItem


@api_view(['GET'])
def missing_items_readings(request):
    time_threshold = datetime.now() - timedelta(seconds=settings.RFID_READING_CYCLE + 10)

    data = LastReadingsSnapshot.objects.filter(
        timestamp_reading__lt=time_threshold
    ).select_related('sku').select_related('antenna', 'position')

    response = {"data": []}
    for row in data:
        try:
            response["data"].append(
                {'sku': row.sku.display_name, 'position_name': row.position.name, 'serial': row.epc}
            )
        except Exception as e:
            print("could not add missing", row.epc)  # this should be using logging
    return Response(response)


@api_view(['GET'])
def reading_zones_summary(request):
    items = Item.objects.all().values_list('epc', flat=True)  # This is not efficient
    time_threshold = datetime.now() - timedelta(seconds=settings.RFID_READING_CYCLE)
    data = LastReadingsSnapshot.objects.filter(
        epc__in=items,
        antenna_id__in=[1, 3],
    ).values(
        'antenna', 'antenna__name', 'position', 'position__name'
    ).annotate(
        total=Count('antenna', filter=Q(timestamp_reading__gte=time_threshold))
    ).order_by('total')

    # {'antenna': 1, 'antenna__name': 'AL200-Z1', 'total': 51}
    response = {"data": []}
    for row in data:
        try:
            response["data"].append(
                {'antenna': row["antenna"], 'position__name': row["position__name"], 'total': row["total"]}
            )
        except Exception as e:
            print("could not add reading", row.epc)  # this should be use logging

    return Response(response)


def transfer_order_coordinates(request):
    transfer_order_id = request.GET.get('transfer_order_id', None)
    include_history = request.GET.get('include_history', False)

    if transfer_order_id and include_history:
        data = TransferOrderTracking.objects.filter(order_id=transfer_order_id).order_by('timestamp_reading')

        coordinates = []
        for row in data:
            coordinates.append([row.longitude, row.latitude])

        response = {"type": "FeatureCollection",
                    "features": [{"type": "Feature", "geometry": {"type": "LineString", "coordinates": coordinates}}]}

    elif transfer_order_id:
        data = TransferOrderTracking.objects.filter(order_id=transfer_order_id).order_by('-timestamp_reading').first()
        if not data:
            return JsonResponse({}, safe=False, status=404)
        response = {"geometry": {"type": "Point", "coordinates": [data.longitude, data.latitude]}, "type": "Feature",
                    "properties": {}}
    else:
        return JsonResponse({}, safe=False, status=404)

    return JsonResponse(response, safe=False, status=200)


@api_view(['POST'])
def test_rfid_readings(request):
    actions = {
        1: 'READ',
        2: 'OUT',
        3: 'READ'
    }
    readings = request.data
    reader = Reader.objects.first()
    reads = []
    now = datetime.now()
    for read in readings:
        item = Item.objects.filter(epc=read.get('data').get('idHex')).first()
        if not item:
            return Response(status=status.HTTP_404_NOT_FOUND)
        antenna = ReaderAntenna.objects.filter(
            serial_number=read.get('data').get('antenna')
        ).select_related('position').first()
        item.current_position = antenna.position
        match antenna.id:
            case 1 | 3:
                item.last_seen_timestamp = now
                item.last_seen_action = 'READ'
                item.save()
            case 2:
                update_transfer_order(item, now)

        reads.append(
            Reading(
                epc=read.get('data').get('idHex'),
                antenna_id=antenna.id,
                node_id=read.get('node', Node.objects.first().id),
                reader_id=reader.id,
                timestamp_reading=now,
                action=actions.get(antenna.id)
            )
        )
    Reading.objects.bulk_create(reads)
    return Response(status=status.HTTP_200_OK)


def update_transfer_order(item, current_time):
    transfer_item = TransferOrderItem.objects.filter(item=item).first()
    if transfer_item:
        order = transfer_item.order
        order.state = 'IP'
        transfer_item.state = 'EN'
        transfer_item.save()
        order.save()
        if not order.transferorderitem_set.filter(state__in=['RE', 'NOE']).exists():
            order.state = 'CO'
            order.actual_completion_date = current_time
            order.save()

    item.last_seen_timestamp = current_time
    item.last_seen_action = 'OUT'
    item.in_transit = True
    item.save()


