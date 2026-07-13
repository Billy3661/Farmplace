from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, FarmerProfile


class FarmerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = [
            'phone', 'county', 'sub_county', 'farm_name', 'farm_type',
            'farm_size', 'bio', 'avatar', 'whatsapp', 'years_experience',
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'county': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_county': forms.TextInput(attrs={'class': 'form-control'}),
            'farm_name': forms.TextInput(attrs={'class': 'form-control'}),
            'farm_type': forms.Select(attrs={'class': 'form-control'}),
            'farm_size': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'years_experience': forms.NumberInput(attrs={'class': 'form-control'}),
        }
