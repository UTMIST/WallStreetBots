from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework import status

from .apimanagers import APImanager
from .models import Stock, Order, Portfolio


def index(request):
    # ALPACA SECRET KEY
    return HttpResponse("Hello World, welcome to tradingbot!")


@login_required
def stock_trade(request):
    user = request.user
    transaction_side = request.POST.get('transaction_side')
    transaction_type = request.POST.get('transaction_type')
    ticker = request.POST.get('ticker')
    # price is used for other order types, commented out for linter for now
    # price = float(request.POST.get('price')) if request.POST.get('price') else None
    portfolio_name = request.POST.get('portfolio')
    alpaca_api = APImanager(user.credential.alpaca_id, user.credential.alpaca_key)
    quantity = int(request.POST.get('quantity'))

    if transaction_side == 'sell':
        return HttpResponse(status=status.HTTP_501_NOT_IMPLEMENTED)

    if transaction_side == 'buy':
        if transaction_type == 'market':
            if not alpaca_api.market_buy(ticker, quantity):
                return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            portfolio_name = Portfolio.objects.get(user=user, name=portfolio_name)
            stock = Stock.objects.get(ticker=ticker)
            order = Order(
                user=user,
                stock=stock,
                quantity=quantity,
                portfolio=portfolio_name,
                transaction_type=transaction_type,
                transaction_side=transaction_side
            )
            order.save()
            return HttpResponse(status=status.HTTP_201_CREATED)

        return HttpResponse(status=status.HTTP_501_NOT_IMPLEMENTED)
