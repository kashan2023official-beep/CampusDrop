from django import forms
from .models import Order
from .utils import is_inside_campus


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'pickup_lat',
            'pickup_lon',
            'pickup_label',
            'dropoff_lat',
            'dropoff_lon',
            'dropoff_label',
            'weight_kg',
            'item_type',
            'notes',
        ]
        widgets = {
            'pickup_lat': forms.HiddenInput(),
            'pickup_lon': forms.HiddenInput(),
            'pickup_label': forms.TextInput(
                attrs={
                    'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-gray-50',
                    'placeholder': 'Select on map...',
                    'readonly': 'readonly'
                }
            ),
            'dropoff_lat': forms.HiddenInput(),
            'dropoff_lon': forms.HiddenInput(),
            'dropoff_label': forms.TextInput(
                attrs={
                    'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-gray-50',
                    'placeholder': 'Select on map...',
                    'readonly': 'readonly'
                }
            ),
            'weight_kg': forms.NumberInput(
                attrs={
                    'step': '0.1',
                    'min': '0.1',
                    'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500',
                    'placeholder': 'e.g. 1.5',
                }
            ),
            'item_type': forms.Select(
                attrs={
                    'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3,
                    'class': 'w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500',
                    'placeholder': 'Optional handling instructions (e.g. Fragile)',
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        pickup_lat = cleaned_data.get('pickup_lat')
        pickup_lon = cleaned_data.get('pickup_lon')
        dropoff_lat = cleaned_data.get('dropoff_lat')
        dropoff_lon = cleaned_data.get('dropoff_lon')

        if pickup_lat is not None and pickup_lon is not None:
            if not is_inside_campus(pickup_lat, pickup_lon):
                self.add_error('pickup_lat', 'Pickup location must be inside campus bounds.')
                raise forms.ValidationError("Pickup location must be within campus bounds.")

        if dropoff_lat is not None and dropoff_lon is not None:
            if not is_inside_campus(dropoff_lat, dropoff_lon):
                self.add_error('dropoff_lat', 'Dropoff location must be inside campus bounds.')
                raise forms.ValidationError("Dropoff location must be within campus bounds.")

        return cleaned_data
