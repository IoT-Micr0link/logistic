"""RFID App Urls"""

from django.urls import path
from . import views as rfid_views

urlpatterns = [
    path('readers/', rfid_views.ReadersListView.as_view(), name='rfid-readers'),
    path('readings/', rfid_views.ReadingsListView.as_view(), name='rfid-readings')
]

