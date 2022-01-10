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
    TIMEINFORCE = [
        ('day', 'Day'),
        ('gtc', 'Good Until Canceled'),
    ]
    ticker = forms.CharField(help_text='Stock ticker')
    order_type = forms.ChoiceField(choices=ORDERTYPES, help_text='Order Type')
    transaction_type = forms.ChoiceField(choices=TRANSACTIONTYPES, help_text='Transaction Type')
    quantity = forms.DecimalField(decimal_places=2, help_text='Quantity')
    time_in_force = forms.ChoiceField(choices=TIMEINFORCE, help_text='Time in force')

    def place_order(self, user, user_details):
        ticker = self.cleaned_data['ticker'].upper()
        order_type = self.cleaned_data['order_type']
        transaction_type = self.cleaned_data['transaction_type']
        quantity = self.cleaned_data['quantity']
        time_in_force = self.cleaned_data['time_in_force']
        from backend.tradingbot.apiutility import place_general_order
        try:
            place_general_order(user=user, user_details=user_details, ticker=ticker, quantity=quantity,
                                order_type=order_type,
                                transaction_type=transaction_type, time_in_force=time_in_force)
            return "Order placed successfully"
        except Exception as e:
            return str(e)
