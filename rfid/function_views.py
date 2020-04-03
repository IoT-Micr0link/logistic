from django.http import JsonResponse
from rfid.view_models import *
from django.db.models import Count

# this views should be a REST API in the future, consideted using DRF

def reading_zones_summary(request):
    data = LastReadingsSnapshot.objects.all().values('antenna', 'antenna__name')\
            .annotate(total=Count('antenna')).order_by('total')

    #{'antenna': 1, 'antenna__name': 'AL200-Z1', 'total': 51}
    response = {
        "data":[]
    }
    for row in data:
        response["data"].append(
            {'antenna': row["antenna"], 'antenna__name': row["antenna__name"],  'total': row["total"]}
        )
    return JsonResponse(response, safe=False)


def transfer_order_coordinates(request):
    transfer_order_id = request.GET.get('transfer_order_id',None)
    include_history = request.GET.get('include_history', False)


    if transfer_order_id and include_history:
        data = TransferOrderTracking.objects.filter(order_id=transfer_order_id).order_by('timestamp_reading')

        coordinates = []
        for row in data:
            coordinates.append([row.longitude,row.latitude])

        response = { "type": "FeatureCollection",
                    "features": [{"type": "Feature", "geometry": { "type": "LineString", "coordinates": coordinates}}]}

    elif transfer_order_id:
        data = TransferOrderTracking.objects.filter(order_id=transfer_order_id).order_by('-timestamp_reading').first()
        if not data:
            return JsonResponse({}, safe=False, status=404)
        response = {"geometry": {"type": "Point", "coordinates": [data.longitude, data.latitude]}, "type": "Feature", "properties": {}}
    else:
        return JsonResponse({}, safe=False, status=404)

    return JsonResponse(response, safe=False, status=200)