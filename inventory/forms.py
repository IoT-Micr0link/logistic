

class SKUfilterForm(forms.ModelForm):
    id_to = forms.ModelChoiceField(
        queryset=SKU.objects.all(),
        required=False,
        label="Hasta referencia",
        widget=autocomplete.ModelSelect2(
            url='sku-autocomplete',
            attrs={
               'language': 'es',
               'data-placeholder': 'Digite ...',
               'data-minimum-input-length': 2,
            },
        )
    )

    id_from = forms.ModelChoiceField(
        queryset=SKU.objects.all(),
        required=False,
        label="Desde referencia",
        widget=autocomplete.ModelSelect2(
            url='sku-autocomplete',
            attrs={
                'language': 'es',
                'data-placeholder': 'Digite ...',
                'data-minimum-input-length': 2,
            },
        )
    )

    class Meta:
        model = SKU
        fields = ['display_name']


class ItemFilterForm(forms.ModelForm):
    id_to = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        required=False,
        label="Hasta referencia",
        widget=autocomplete.ModelSelect2(
           url='item-autocomplete',
           attrs={
               'language': 'es',
               'data-placeholder': 'Digite ...',
               'data-minimum-input-length': 2,
           },
       )
    )
    id_from = forms.ModelChoiceField(
        queryset=Item.objects.all(), required=False,
        label="Desde referencia",
        widget=autocomplete.ModelSelect2(
            url='item-autocomplete',
            attrs={
                'language': 'es',
                'data-placeholder': 'Digite ...',
                'data-minimum-input-length': 2,
            },
        )
    )

    class Meta:
        model = Item
        fields = ['display_name']


class InventorySummaryFilterForm(forms.Form):
    sku_id_from = forms.ModelChoiceField(queryset=SKU.objects.all(), required=False, label="Desde referencia",
                                         widget=autocomplete.ModelSelect2(
                                             url='sku-autocomplete',
                                             attrs={
                                                 'language': 'es',
                                                 'data-placeholder': 'Digite ...',
                                                 'data-minimum-input-length': 2,
                                             },
                                         )
                                         )

    sku_id_to = forms.ModelChoiceField(queryset=SKU.objects.all(), required=False, label="Hasta referencia",
                                       widget=autocomplete.ModelSelect2(
                                           url='sku-autocomplete',
                                           attrs={
                                               'language': 'es',
                                               'data-placeholder': 'Digite ...',
                                               'data-minimum-input-length': 2,

                                           },
                                       )
                                       )

    sku_id = forms.ModelChoiceField(queryset=SKU.objects.all(), required=False, label="Referencia",
                                    widget=autocomplete.ModelSelect2(
                                        url='sku-autocomplete',
                                        attrs={
                                            'language': 'es',
                                            'data-placeholder': 'Digite ...',
                                            'data-minimum-input-length': 2,

                                        },
                                    )
                                    )

    location_id_from = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label="Desde bodega ",
                                              widget=autocomplete.ModelSelect2(
                                                  url='location-autocomplete',
                                                  attrs={
                                                      'language': 'es',
                                                      'data-placeholder': 'Digite ...',
                                                      'data-minimum-input-length': 2,

                                                  },
                                              )
                                              )

    location_id_to = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label="Hasta bodega ",
                                            widget=autocomplete.ModelSelect2(
                                                url='location-autocomplete',
                                                attrs={
                                                    'language': 'es',
                                                    'data-placeholder': 'Digite ...',
                                                    'data-minimum-input-length': 2,

                                                },
                                            )
                                            )

    location_id = forms.ModelChoiceField(queryset=Location.objects.all(), required=False, label="Bodega ",
                                         widget=autocomplete.ModelSelect2(
                                             url='location-autocomplete',
                                             attrs={
                                                 'language': 'es',
                                                 'data-placeholder': 'Digite ...',
                                                 'data-minimum-input-length': 2,

                                             },
                                         )
                                         )

    all_locations = forms.BooleanField(required=False, label="Incluir todas las bodegas")
    all_skus = forms.BooleanField(required=False, label="Incluir todas las referencias")

    class Meta:
        model = InventorySummary
        fields = ('sku_id', 'location_id')