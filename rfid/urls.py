"""RFID App Urls"""

from django.urls import path
from . import views as rfid_views

urlpatterns = [
    path('inventory/', rfid_views.ItemListView.as_view(), name='item-inventory'),
    path('inventory/sku/', rfid_views.SKUInventoryView.as_view(),
         name='inventory-sku'),
    path('inventory/items-inventory-location/', rfid_views.LocationInventoryView.as_view(),
         name='item-inventory-location'),
    path('inventory/<int:pk>/sku_detail/', rfid_views.SKUDetailView.as_view(), name='sku_detail'),

    path('inventory/<str:pk>/detail/', rfid_views.ItemDetailView.as_view(), name='item-detail'),
    path('transfer-orders/', rfid_views.TransferOrderListView.as_view(),
         name='transfer-order-list'),
    path('transfer-orders/<int:id_order>/detail/',
         rfid_views.TransferOrderDetailView.as_view(), name='transfer-order-detail'),
    path('warehouse-entries/', rfid_views.WarehouseEntryListView.as_view(),
         name='warehouse-entry-list'),
    path('warehouse-entries/<int:id_entry>/detail/',
         rfid_views.WarehouseEntryDetailView.as_view(), name='warehouse-entry-detail'),
    path('transfer-orders-tracking/', rfid_views.TrackingTransfersView.as_view(), name='tracking-transfer-orders'),
    path('warehouse-tracking/', rfid_views.TrackingWarehouseView.as_view(), name='tracking-warehouse'),
]

