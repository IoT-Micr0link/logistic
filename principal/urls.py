"""principal URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from iot import views as iot_views
from rfid import views as rfid_views
from rest_api import urls as rest_api_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', iot_views.DashboardView.as_view(), name='index'),

    # URLS LOGISTICS (Include rfid.urls)

    path('logistics/', include(('rfid.urls', 'rfid'), namespace='logistics')),

    # REST API URL (Include rest_api.url)

    path('rest_api/', include(('rest_api.urls', 'rest_api'), namespace='rest_api')),

    #Autocomplete
    path('autocomplete/skus/', rfid_views.SKUAutocomplete.as_view(), name='sku-autocomplete'),
    path('autocomplete/locations/', rfid_views.LocationAutocomplete.as_view(), name='location-autocomplete'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)