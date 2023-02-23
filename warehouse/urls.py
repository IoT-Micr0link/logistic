from django.urls import path
from warehouse import views

urlpatterns = [
    path('transfer-orders/', views.TransferOrderListView.as_view(),
         name='transfer-order-list'),
    path('transfer-orders/create/', views.CreateTransferOrder.as_view(), name='create_transfer_order'),
    path('transfer-orders/<int:id_order>/detail/',
         views.TransferOrderDetailView.as_view(), name='transfer-order-detail'),
    path('entries/', views.WarehouseEntryListView.as_view(),
         name='warehouse-entry-list'),
    path('entries/<int:id_entry>/detail/',
         views.WarehouseEntryDetailView.as_view(), name='warehouse-entry-detail'),
    path('transfer-orders/tracking/', views.TrackingTransfersView.as_view(), name='tracking-transfer-orders'),
    path('tracking/', views.TrackingWarehouseView.as_view(), name='tracking-warehouse'),
]
