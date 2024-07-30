# forms.py
from django import forms
from .models import InventoryItem, Technician

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['barcode', 'equipment_name', 'checked_in']  # Include checked_in field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Additional initialization if needed


class CheckInOutForm(forms.Form):
    barcode = forms.CharField(max_length=100, required=True)
    technician_name = forms.ModelChoiceField(
        queryset=Technician.objects.none(),
        required=False,  # Only required when checking out an item
        empty_label="Select Technician"
    )

    def __init__(self, *args, **kwargs):
        technicians = kwargs.pop('technicians', None)
        super().__init__(*args, **kwargs)
        if technicians is not None:
            self.fields['technician_name'].queryset = technicians