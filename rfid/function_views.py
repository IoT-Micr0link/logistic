from django.http import JsonResponse
from rfid.view_models import *
from django.db.models import Count


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