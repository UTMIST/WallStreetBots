def sync_alpaca(user):
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
    user_details['equity'] = account.equity
    user_details['buy_power'] = account.buying_power
    user_details['cash'] = account.cash
    user_details['currency'] = account.currency
    user_details['long_portfolio_value'] = account.long_market_value
    user_details['short_portfolio_value'] = account.short_market_value

    # get portfolio information
    portfolio = api.get_positions()

    # non-user specific synchronization. e.g. add new company, new stock if it didn't exist
    from backend.tradingbot.models import Company, Stock
    for position in portfolio:
        # print(position)
        if not Company.objects.filter(ticker=position.symbol).exists():
            # add Company
            company = Company(name=position.symbol, ticker=position.symbol)
            company.save()
            # add Stock
            stock = Stock(company=company)
            stock.save()
            print(f"added {position.symbol} to Company and Stock")

    # print(account)
    # user-specific synchronization
    # 1) check if user has a portfolio and update portfolio cash
    if not hasattr(user, 'portfolio'):
        from .models import Portfolio
        port = Portfolio(user=user, cash=account.cash, name='default-1')
        port.save()
        print("created portfolio default-1 for user")
    else:
        user.portfolio.cash = account.cash
        user.portfolio.save()

    # 2) synchronizes user's stock instances
    # brute force way to delete and add all new stocks
    from backend.tradingbot.models import StockInstance, Stock, Company
    StockInstance.objects.filter(portfolio=user.portfolio).delete()
    for position in portfolio:
        company = Company.objects.get(ticker=position.symbol)
        stock = Stock.objects.get(company=company)
        instance = StockInstance(stock=stock, portfolio=user.portfolio, quantity=position.qty, user=user)
        instance.save()

    # 3) synchronizes order status (To be completed)

    user_details['portfolio'] = portfolio
    return user_details
