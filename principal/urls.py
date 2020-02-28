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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', iot_views.DashboardView.as_view(), name='index'),
    path('logistica/inventory/', rfid_views.ItemListView.as_view(), name='logistica-inventory'),
    path('logistica/transfer-orders/', rfid_views.TransferOrderListView.as_view(), name='logistica-transfer-order-list'),
    path('logistica/transfer-orders/<int:id_order>/detail',
         rfid_views.TransferOrderDetailView.as_view(), name='logistica-transfer-order-detail'),
    path('rfid/readers/', rfid_views.ReadersListView.as_view(), name='rfid-reader-list'),
    path('rfid/readings/', rfid_views.ReadingsListView.as_view(), name='rfid-readings-list'),


]

