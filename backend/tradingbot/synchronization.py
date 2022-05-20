from alpaca_trade_api.rest import APIError


def validate_backend():
    from backend.settings import BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY
    from backend.tradingbot.apimanagers import AlpacaManager
    from django.core.exceptions import ValidationError
    backendapi = AlpacaManager(BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY)
    if not backendapi.validate_api()[0]:
        raise ValidationError(backendapi.validate_api()[1])
    return backendapi


def sync_database_company_stock(ticker):
    """
        check if company/stock for this ticker exist and sync to database if not already exists
        returns the stock and company
    """
    from backend.tradingbot.models import Company, Stock
    if not Company.objects.filter(ticker=ticker).exists():
        # add Company
        company = Company(name=ticker, ticker=ticker)
        company.save()
        # add Stock
        stock = Stock(company=company)
        stock.save()
        print(f"added {ticker} to Company and Stock")
    else:
        company = Company.objects.get(ticker=ticker)
        stock = Stock.objects.get(company=company)
    return stock, company


def sync_alpaca(user):  # noqa: C901
    """
        sync user related database data with Alpaca
        this is a simplified, incomplete version.
    """
    user_details = {}
    # check if user has credential
    if not hasattr(user, 'credential'):
        return

    from backend.tradingbot.apimanagers import AlpacaManager
    api = AlpacaManager(user.credential.alpaca_id, user.credential.alpaca_key)

    # check if api is valid
    if not api.validate_api()[0]:
        print(api.validate_api()[1])
        return

    # get account information
    account = api.get_account()
    user_details['equity'] = str(round(float(account.equity), 2))
    user_details['buy_power'] = str(round(float(account.buying_power), 2))
    user_details['cash'] = str(round(float(account.cash), 2))
    user_details['currency'] = account.currency
    user_details['long_portfolio_value'] = str(round(float(account.long_market_value), 2))
    user_details['short_portfolio_value'] = str(round(float(account.short_market_value), 2))
    user_details['portfolio_percent_change'] = str(round((float(account.portfolio_value) - float(account.last_equity))
                                                         / float(account.last_equity), 2))
    user_details['portfolio_dollar_change'] = str(round((float(account.portfolio_value) - float(account.last_equity))))

    if (float(account.portfolio_value) - float(account.last_equity)) >= 0:
        user_details['portfolio_change_direction'] = "positive"
    elif (float(account.portfolio_value) - float(account.last_equity)) < 0:
        user_details['portfolio_change_direction'] = "negative"
    else:
        user_details['portfolio_change_direction'] = "error"

    user_details['portfolio_percent_change'] = str(
        round((float(account.portfolio_value) - float(account.last_equity)) / float(account.last_equity), 2))
    # get portfolio information
    portfolio = api.get_positions()

    # non-user specific synchronization. e.g. add new company, new stock if it didn't exist
    for position in portfolio:
        sync_database_company_stock(position.symbol)

    from backend.tradingbot.models import StockInstance, Stock, Company, Portfolio
    if not hasattr(user, 'portfolio'):
        new_portfolio = Portfolio(name='default-1', user=user, cash=0)
        new_portfolio.save()
    if StockInstance.objects.filter(user=user, portfolio=user.portfolio).exists():
        StockInstance.objects.filter(user=user, portfolio=user.portfolio).delete()
    for position in portfolio:
        company = Company.objects.get(ticker=position.symbol)
        stock = Stock.objects.get(company=company)
        instance = StockInstance(stock=stock, portfolio=user.portfolio, quantity=position.qty, user=user)
        instance.save()

    # 2) synchronizes order status (To be completed)
    alpaca_open_orders = api.api.list_orders(status='open', nested=True)
    from backend.tradingbot.models import Order
    from backend.tradingbot.apiutility import create_local_order
    local_open_orders = Order.objects.filter(user=user, status='A')
    for order in local_open_orders.iterator():
        client_order_id = str(order.order_number)
        try:
            if order.client_order_id == '':
                alpaca_order = api.api.get_order_by_client_order_id(client_order_id)
            else:
                alpaca_order = api.api.get_order_by_client_order_id(order.client_order_id)
        except APIError:
            print(f"Order ID {client_order_id} deleted as no matching order found in Alpaca")
            order.delete()
            continue
        if alpaca_order.status == 'accepted':
            order.status = 'A'
        elif alpaca_order.status == 'new':
            order.status = 'N'
        elif alpaca_order.status == 'filled':
            order.status = 'F'
            order.filled_avg_price = float(alpaca_order.filled_avg_price)
            order.filled_timestamp = alpaca_order.filled_at.to_pydatetime()
            order.filled_quantity = float(alpaca_order.filled_qty)
        else:  # order closed, either cancelled or completed
            order.status = 'C'
        order.save()

    usable_cash = float(account.cash)
    for order in alpaca_open_orders:
        # get usable trading cash
        if order.order_type == 'market' and order.side == 'buy':
            backendapi = validate_backend()
            _, price = backendapi.get_price(order.symbol)
            # print(f"{order.symbol}, {price}")
            usable_cash -= float(price) * float(order.qty)
        # sync open orders to database if not already exist
        if not order.client_order_id.isnumeric() or \
                not Order.objects.filter(user=user, order_number=order.client_order_id).exists():
            if not Order.objects.filter(user=user, client_order_id=order.client_order_id).exists():
                create_local_order(user=user, ticker=order.symbol, quantity=float(order.qty),
                                   order_type=order.order_type, transaction_type=order.side, status="A",
                                   client_order_id=order.client_order_id)

    user_details['usable_cash'] = str(round(usable_cash, 2))
    user_details['portfolio'] = portfolio
    user_details['orders'] = [order.display_order() for order in
                              Order.objects.filter(user=user).order_by('-timestamp').iterator()]

    # 3) check if user has a portfolio and update portfolio cash
    if not hasattr(user, 'portfolio'):
        from .models import Portfolio
        port = Portfolio(user=user, cash=float(user_details['usable_cash']), name='default-1')
        port.save()
        print("created portfolio default-1 for user")
    else:
        user.portfolio.cash = float(user_details['usable_cash'])
        user.portfolio.save()
    user_details['strategy'] = {
        'rebalance': user.portfolio.rebalancing_strategy,
        'optimization': user.portfolio.optimization_strategy,
    }

    return user_details
