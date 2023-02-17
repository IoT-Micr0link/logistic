from django.forms import forms

from reports.models import InventoryRequest


class InventoryRequestForm(forms.ModelForm):
    class Meta:
        model = InventoryRequest
        fields = ['wait_minutes', 'init_sku', 'end_sku', 'init_location', 'end_location', 'all_locations', 'all_skus']
        labels = {
            'wait_minutes': 'Tiempo espera (mins)',
            'init_sku': 'Desde referencia',
            'end_sku': 'Hasta referencia',
            'init_location': 'Desde bodega',
            'end_location': 'Hasta bodega',
            'all_locations': 'Todas las bodegas',
            'all_skus': 'Todas las referencias',
        }