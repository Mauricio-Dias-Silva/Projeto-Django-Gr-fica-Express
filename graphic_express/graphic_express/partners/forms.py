# partners/forms.py
from django import forms
from .models import Partner

class PartnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = [
            'company_name', 'cnpj', 'specialization', 'capacity',
            'address', 'city', 'state', 'zip_code', 'delivery_radius_km', 'description'
        ]
