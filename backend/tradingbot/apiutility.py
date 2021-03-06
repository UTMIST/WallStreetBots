from django.core.exceptions import ValidationError

from backend.tradingbot.apimanagers import AlpacaManager
from backend.tradingbot.synchronization import validate_backend, sync_database_company_stock, sync_stock_instance


def create_local_order(user, ticker, quantity, order_type, transaction_type, status, client_order_id=''):
    if transaction_type == 'buy':
        transaction_type = 'B'
    elif transaction_type == 'sell':
        transaction_type = 'S'
    else:
        raise ValidationError("invalid transaction type")
    if order_type == 'market':
        order_type = 'M'
    else:
        raise ValidationError("invalid order type")

    stock, _ = sync_database_company_stock(ticker)
    from backend.tradingbot.models import Order
    order = Order(user=user, stock=stock, order_type=order_type,
                  quantity=quantity, transaction_type=transaction_type,
                  status=status, client_order_id=client_order_id)
    order.save()


def place_general_order(user, user_details, ticker, quantity, transaction_type, order_type, time_in_force):
    """
    General place order function that takes account of database, margin, and alpaca synchronization.
    supports market buy/sell
    user: request.user
    user_details: return from sync_alpaca function
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
    """
    backend_api = validate_backend()
    user_api = AlpacaManager(user.credential.alpaca_id, user.credential.alpaca_key)

    # 1. check if ticker exists and check buy / sell availability and errors
    check, price = backend_api.get_price(ticker)
    if not check:
        raise ValidationError(f'Failed to get price for {ticker}, are you sure that the ticker name is correct?')
    if transaction_type == 'B':
        a_transaction_type = 'buy'
        a_order_type = buy_order_check(order_type=order_type, price=price, quantity=quantity,
                                       usable_cash=user_details['usable_cash'])
    elif transaction_type == 'S':
        a_transaction_type = 'sell'
        a_order_type = sell_order_check(order_type=order_type, price=price, quantity=quantity,
                                        usable_cash=user_details['usable_cash'])
    else:
        raise ValidationError("invalid transaction type")

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
            time_in_force=time_in_force,
            client_order_id=str(client_order_id)
        )
    except Exception as e:
        # 4. delete order if not valid.
        order.delete()
        raise ValidationError(e)

    return True


def add_stock_to_database(user, ticker):
    # 1. check if ticker exists
    ticker = ticker.upper()
    backend_api = validate_backend()
    check, price = backend_api.get_price(ticker)
    if not check:
        raise ValidationError(f'Failed to get price for {ticker}, are you sure that the ticker name is correct?')
    stock, _ = sync_database_company_stock(ticker)
    sync_stock_instance(user, user.portfolio, stock)


def buy_order_check(order_type, price, quantity, usable_cash):
    a_order_type = ''
    if order_type == 'M':
        a_order_type = 'market'
        if float(price) * float(quantity) > float(usable_cash):
            raise ValidationError('Not enough cash to perform this operation. Marginal trading is not supported.')
    elif order_type == 'L':
        pass
    elif order_type == 'S':
        pass
    elif order_type == 'ST':
        pass
    elif order_type == 'T':
        pass
    return a_order_type


def sell_order_check(order_type, price, quantity, usable_cash):
    a_order_type = ''
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
    return a_order_type
