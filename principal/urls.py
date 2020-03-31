"""principal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from iot import views as iot_views
from rfid import views as rfid_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', iot_views.DashboardView.as_view(), name='index'),
    path('logistics/inventory/items-inventory-sku/', rfid_views.ItemInventoryView.as_view(), name='logistics-item-inventory-sku'),
    path('logistics/inventory/items-inventory-location/', rfid_views.LocationInventoryView.as_view(), name='logistics-item-inventory-location'),

    path('logistics/inventory/skus/', rfid_views.SKUListView.as_view(), name='logistics-sku-inventory'),
    path('logistics/inventory/skus/<int:pk>/detail/', rfid_views.SKUDetailView.as_view(), name='logistics-sku-detail'),
    path('logistics/transfer-orders/', rfid_views.TransferOrderListView.as_view(), name='logistics-transfer-order-list'),
    path('logistics/transfer-orders/<int:id_order>/detail/',
         rfid_views.TransferOrderDetailView.as_view(), name='logistics-transfer-order-detail'),

    path('logistics/warehouse-entries/', rfid_views.WarehouseEntryListView.as_view(),
         name='logistics-warehouse-entry-list'),
    path('logistics/warehouse-entries/<int:id_entry>/detail/',
         rfid_views.WarehouseEntryDetailView.as_view(), name='logistics-warehouse-entry-detail'),

    path('rfid/readers/', rfid_views.ReadersListView.as_view(), name='rfid-reader-list'),
    path('rfid/readings/', rfid_views.ReadingsListView.as_view(), name='rfid-readings-list'),

    #Autocomplete
    path('autocomplete/skus/', rfid_views.SKUAutocomplete.as_view(), name='sku-autocomplete'),
    path('autocomplete/locations/', rfid_views.LocationAutocomplete.as_view(), name='location-autocomplete'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)