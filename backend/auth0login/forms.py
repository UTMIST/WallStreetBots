from django import forms
from .models import Credential


class CredentialModelForm(forms.ModelForm):
    class Meta:
        model = Credential
        fields = [
            'user',
            'alpaca_id',
            'alpaca_key'
        ]
