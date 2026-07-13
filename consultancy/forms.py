from django import forms
from .models import ConsultationBooking


class ConsultationBookingForm(forms.ModelForm):
    class Meta:
        model = ConsultationBooking
        fields = [
            'consultation_type', 'preferred_date', 'preferred_time',
            'phone', 'farm_location', 'description',
        ]
        widgets = {
            'consultation_type': forms.Select(attrs={'class': 'form-control'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'farm_location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
