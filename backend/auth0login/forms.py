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

    def place_order(self, user, user_details):
        ticker = self.cleaned_data['ticker'].upper()
        order_type = self.cleaned_data['order_type']
        transaction_type = self.cleaned_data['transaction_type']
        quantity = self.cleaned_data['quantity']
        from backend.tradingbot.apiutility import place_general_order
        try:
            place_general_order(user=user, user_details=user_details, ticker=ticker, quantity=quantity, order_type=order_type,
                                transaction_type=transaction_type)
            return "Order placed successfully"
        except Exception as e:
            return str(e)
