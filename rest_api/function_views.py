from datetime import datetime

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response

from rfid.view_models import *
from django.db.models import Count

from rest_framework.decorators import api_view

# this views should be a REST API in the future, consider using DRF


def missing_items_readings(request):
    time_threshold = timezone.now() - timedelta(minutes=settings.RFID_READING_CYCLE)

    data = LastReadingsSnapshot.objects.filter(
        timestamp_reading__lt=time_threshold
    ).select_related('sku').select_related('antenna')

    response = {
        "data": []
    }
    for row in data:
        try:
            response["data"].append(
                {'sku': row.sku.display_name, 'antenna_name': row.antenna.name, 'serial': row.epc}
            )
        except Exception as e:
            print("could not add missing", row.epc)  # this shlud be ussing logging
    return JsonResponse(response, safe=False)


def reading_zones_summary(request):
    items = Item.objects.all().values_list('epc', flat=True)  # This is not efficent
    time_threshold = timezone.now() - timedelta(minutes=settings.RFID_READING_CYCLE)
    data = LastReadingsSnapshot.objects.filter(
        #timestamp_reading__gte=time_threshold,
        epc__in=items
    ).values('antenna', 'antenna__name') \
        .annotate(total=Count('antenna')).order_by('total')

    # {'antenna': 1, 'antenna__name': 'AL200-Z1', 'total': 51}
    response = {
        "data": []
    }
    for row in data:
        try:
            response["data"].append(
                {'antenna': row["antenna"], 'antenna__name': row["antenna__name"], 'total': row["total"]}
            )
        except Exception as e:
            print("could not add reading", row.epc)  # this should be use logging

    return JsonResponse(response, safe=False)


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
    print(request.data)
    data = request.data
    timestamp = datetime.fromtimestamp(data.get('timestamp'))
    readings = data.get('readings', [])
    reads = [
        Reading(
            epc=read,
            antenna_id=data.get('antenna'),
            node_id=data.get('node_id'),
            reader_id=data.get('reader_id', 1),
            timestamp_reading=timestamp
        )
        for read in readings
    ]
    Reading.objects.bulk_create(reads)
    return Response(data, status=status.HTTP_200_OK)