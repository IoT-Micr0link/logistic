import django.forms as forms
from rfid.view_models import *
from dal import autocomplete

class InventoryRequestForm(forms.ModelForm):
    class Meta:
         model = InventoryRequest
         fields = ['wait_minutes', 'init_sku', 'end_sku', 'init_location','end_location','all_locations','all_skus']
         labels = {
             'wait_minutes': 'Tiempo espera (mins)',
             'init_sku': 'Desde referencia',
             'end_sku': 'Hasta referencia',
             'init_location': 'Desde bodega',
             'end_location': 'Hasta bodega',
             'all_locations': 'Todas las bodegas',
             'all_skus': 'Todas las referencias',
         }


class InvetorySummaryFilterForm(forms.Form):
    sku_id_from = forms.ModelChoiceField(queryset=SKU.objects.all(),required=False, label="Desde referencia",
        widget=autocomplete.ModelSelect2(
            url='sku-autocomplete',
            attrs={
                'language': 'es',
                'data-placeholder': 'Digite ...',
                'data-minimum-input-length': 2,

            },
        )
    )

    sku_id_to = forms.ModelChoiceField(queryset=SKU.objects.all(),required=False, label="Hasta referencia",
        widget=autocomplete.ModelSelect2(
            url='sku-autocomplete',
            attrs={
                'language': 'es',
                'data-placeholder': 'Digite ...',
                'data-minimum-input-length': 2,

            },
        )
    )

    sku_id = forms.ModelChoiceField(queryset=SKU.objects.all(),required=False, label="Referencia",
        widget=autocomplete.ModelSelect2(
            url='sku-autocomplete',
            attrs={
                'language': 'es',
                'data-placeholder': 'Digite ...',
                'data-minimum-input-length': 2,

            },
        )
    )

    location_id_from = forms.ModelChoiceField(queryset=Location.objects.all(),required=False, label="Desde bodega ",
        widget=autocomplete.ModelSelect2(
            url='location-autocomplete',
            attrs={
                'language': 'es',
                'data-placeholder': 'Digite ...',
                'data-minimum-input-length': 2,

            },
        )
    )

    location_id_to = forms.ModelChoiceField(queryset=Location.objects.all(),required=False, label="Hasta bodega ",
        widget=autocomplete.ModelSelect2(
            url='location-autocomplete',
            attrs={
                'language': 'es',
                'data-placeholder': 'Digite ...',
                'data-minimum-input-length': 2,

            },
        )
    )

    location_id = forms.ModelChoiceField(queryset=Location.objects.all(),required=False, label="Bodega ",
        widget=autocomplete.ModelSelect2(
            url='location-autocomplete',
            attrs={
                'language': 'es',
                'data-placeholder': 'Digite ...',
                'data-minimum-input-length': 2,

            },
        )
    )

    all_locations  = forms.BooleanField(required=False, label="Incluir todas las bodegas")
    all_skus = forms.BooleanField(required=False, label="Incluir todas las referencias")


    class Meta:
        model = InventorySummary
        fields = ('sku_id','location_id')



