"""Rest API Urls"""
from django.urls import path
from . import function_views as rfid_func_views
from rfid.views import ReadersListView, ReadingsListView

urlpatterns = [
    path('readers/', ReadersListView.as_view(), name='rfid-reader-list'),
    path('readings/', ReadingsListView.as_view(), name='rfid-readings-list'),
    path('reading-zones-snapshot/', rfid_func_views.reading_zones_summary, name='reading-zones-snapshot'),
    path('transfer-order-coordinates/', rfid_func_views.transfer_order_coordinates,
         name='transfer-order-coordinates'),
    path('reading-missing-items/', rfid_func_views.missing_items_readings, name='reading-missing-items'),
    path('items-movements/', rfid_func_views.item_movements, name='items-movements'),
    path('readings/zebra/', rfid_func_views.test_rfid_readings, name='readings-zebra')
]
