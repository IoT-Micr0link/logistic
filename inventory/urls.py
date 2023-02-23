from django.urls import path

from inventory import views

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item-inventory'),
    path('sku/', views.SKUInventoryView.as_view(),
         name='inventory-sku'),
    path('items-inventory-location/', views.LocationInventoryView.as_view(),
         name='item-inventory-location'),
    path('<int:pk>/sku_detail/', views.SKUDetailView.as_view(), name='sku_detail'),

    path('<str:pk>/detail/', views.ItemDetailView.as_view(), name='item-detail'),

    # autocompletes
    path('autocomplete/skus/', views.SKUAutocomplete.as_view(), name='sku-autocomplete'),
    path('autocomplete/locations/', views.LocationAutocomplete.as_view(), name='location-autocomplete'),
    path('autocomplete/items', views.ItemAutocomplete.as_view(), name='item-autocomplete')
]