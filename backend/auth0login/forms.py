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
        from backend.tradingbot.synchronization import validate_backend, sync_database_company_stock
        from backend.tradingbot.apimanagers import AlpacaManager
        backend_api = validate_backend()
        user_api = AlpacaManager(user.credential.alpaca_id, user.credential.alpaca_key)

        # 1. check if ticker exists and check buy / sell availability and errors
        check, price = backend_api.get_price(ticker)
        if not check:
            return f'Failed to get price for {ticker}, are you sure that the ticker name is correct?'
        if transaction_type == 'B':
            a_transaction_type = 'buy'
            if order_type == 'M':
                a_order_type = 'market'
                if float(price) * float(quantity) > float(user_details['cash']):
                    return 'Not enough cash to perform this operation. Marginal trading is not supported.'
            elif order_type == 'L':
                pass
            elif order_type == 'S':
                pass
            elif order_type == 'ST':
                pass
            elif order_type == 'T':
                pass
        else:  # transaction_type == 'S'
            a_transaction_type = 'sell'
            if order_type == 'M':
                a_order_type = 'market'
            elif order_type == 'L':
                pass
            elif order_type == 'S':
                pass
            elif order_type == 'ST':
                pass
            elif order_type == 'T':
                pass

        # 2. store order to database
        # 2.1 check if stock and company exists
        stock, _ = sync_database_company_stock(ticker)
        from backend.tradingbot.models import Order
        order = Order(user=user, stock=stock, order_type=order_type,
                      quantity=quantity, transaction_type=transaction_type,
                      status='A')
        order.save()
        client_order_id = order.order_number
        # 3. place order to Alpaca
        try:
            user_api.api.submit_order(
                symbol=ticker,
                qty=float(quantity),
                side=a_transaction_type,
                type=a_order_type,
                time_in_force='gtc',
                client_order_id=str(client_order_id)
            )
        except Exception as e:
            # 4. delete order if not valid.
            order.delete()
            return e

        return "Order placed successfully"  # return empty string if no errors
