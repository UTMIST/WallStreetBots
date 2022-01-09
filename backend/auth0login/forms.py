from django import forms


class CredentialForm(forms.Form):
    """credential for user"""
    alpaca_id = forms.CharField(help_text='Your Alpaca ID')
    alpaca_key = forms.CharField(help_text='Your Alpaca Key')

    def get_id(self):
        return self.cleaned_data['alpaca_id']

    def get_key(self):
        return self.cleaned_data['alpaca_key']


class OrderForm(forms.Form):
    """manual orders from user"""
    ORDERTYPES = [
        ('M', 'Market'),
        # ('L', 'Limit'),
        # ('S', 'Stop'),
        # ('ST', 'Stop Limit'),
        # ('T', 'Trailing Stop'),
    ]
    TRANSACTIONTYPES = [
        ('B', 'Buy'),
        ('S', 'Sell'),
    ]
    ticker = forms.CharField(help_text='Stock ticker')
    order_type = forms.ChoiceField(choices=ORDERTYPES, help_text='Order Type')
    transaction_type = forms.ChoiceField(choices=TRANSACTIONTYPES, help_text='Transaction Type')
    quantity = forms.DecimalField(decimal_places=2, help_text='Quantity')

    def clean_data(self, user):
        ticker = self.cleaned_data['ticker'].upper()
        order_type = self.cleaned_data['order_type']
        transaction_type = self.cleaned_data['transaction_type']
        quantity = self.cleaned_data['quantity']
        from backend.tradingbot.synchronization import validate_backend, sync_alpaca
        from django.core.exceptions import ValidationError
        backendapi = validate_backend()
        # check if the ticker exists
        check, price = backendapi.get_price('ticker')
        if not check:
            raise ValidationError(_(f'Failed to get price for {ticker}, are you sure that the ticker name is correct?'))
        return ticker, order_type, transaction_type, quantity

