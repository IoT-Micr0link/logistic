"""principal URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from iot import views as iot_views
from rfid import views as rfid_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', iot_views.DashboardView.as_view(), name='index'),

    # URLS LOGISTICS (Include rfid.urls)

    path('rfid/', include(('rfid.urls', 'rfid'), namespace='rfid')),
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),
    path('warehouse/', include(('warehouse.urls', 'warehouse'), namespace='warehouse')),
    path('reports/', include(('reports.urls', 'reports'), namespace='reports')),

    # REST API URL (Include rest_api.url)

    path('api/', include(('rest_api.urls', 'rest_api'), namespace='rest_api')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)