"""
Store forms: CheckoutForm
"""
from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone',
            'address_line1', 'address_line2',
            'city', 'state', 'postal_code'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name', 'autocomplete': 'name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address', 'autocomplete': 'email', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10-digit mobile number', 'autocomplete': 'tel', 'required': True}),
            'address_line1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Street Address / House No.', 'autocomplete': 'address-line1', 'required': True}),
            'address_line2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Apartment, suite, unit (optional)', 'autocomplete': 'address-line2'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City', 'autocomplete': 'address-level2', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State / Province', 'autocomplete': 'address-level1', 'required': True}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'PIN Code', 'autocomplete': 'postal-code', 'required': True}),
        }
