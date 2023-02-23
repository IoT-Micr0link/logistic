from django import forms

from inventory.models import Item
from warehouse.models import TransferOrder, TransferOrderItem


class CreateTransferOrderForm(forms.ModelForm):

    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.filter(
            last_seen_action='READ'
        ).exclude(transferorderitem__isnull=False),
        required=False,
        label='Items a transferir',
    )

    class Meta:
        model = TransferOrder
        fields = ['destination', 'expected_completion_date', 'items']
        labels = {
            'destination': 'Bodega o estanteria de destino',
            'expected_completion_date': 'Fecha esperada'
        }

    def save(self, commit=True):
        items = self.cleaned_data.pop('items')
        transfer_order = super(CreateTransferOrderForm, self).save(commit)
        _items = [
            TransferOrderItem(item=item, order=transfer_order)
            for item in items
        ]
        TransferOrderItem.objects.bulk_create(_items)
        return transfer_order.id
