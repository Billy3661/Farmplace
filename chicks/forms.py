from django import forms
from .models import ChickOrder


class ChickOrderForm(forms.ModelForm):
    class Meta:
        model = ChickOrder
        fields = [
            'quantity', 'full_name', 'phone', 'email', 'county', 'sub_county',
            'delivery_address', 'preferred_delivery_date', 'needs_brooding_guide',
            'needs_vaccination_schedule', 'special_notes',
        ]
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'county': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_county': forms.TextInput(attrs={'class': 'form-control'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preferred_delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'needs_brooding_guide': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'needs_vaccination_schedule': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'special_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
