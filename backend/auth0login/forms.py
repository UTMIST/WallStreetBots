from django import forms


class AlpacaIDForm(forms.Form):
    alpaca_id = forms.CharField(help_text='Alpaca ID', max_length=100)
    alpaca_key = forms.CharField(help_text='Alpaca Secret Key', max_length=100)
