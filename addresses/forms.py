from django import forms
from .models import Address

class AddressForm(forms.ModelForm ):
    class Meta:
        model = Address
        # fields = '__all__'

        fields = [
            # 'billing_profile'
            # 'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code',

        ]