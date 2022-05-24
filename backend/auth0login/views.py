from urllib.parse import urlencode
from django.conf import settings
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from backend.tradingbot.synchronization import sync_alpaca
import plotly.graph_objects as go
from datetime import date, timedelta
# Importing the api and instantiating the rest client according to our keys
import alpaca_trade_api as api
import plotly.express as px
import pandas as pd


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'accounts/login.html')


@login_required()
def get_user_information(request):
    # this function will request and sync user information from alpaca given the correct credentials
    user = request.user
    user_details = sync_alpaca(user)  # sync the user with Alpaca and extract details
    auth0user = user.social_auth.get(provider='auth0')
    alpaca_id = user.credential.alpaca_id if hasattr(user, 'credential') else "no alpaca id"
    alpaca_key = user.credential.alpaca_key if hasattr(user, 'credential') else "no alpaca key"

    if user_details is None:
        userdata = {
            'name': user.first_name,
            'alpaca_id': alpaca_id,
            'alpaca_key': "*" * len(alpaca_key),
            'error': "The Alpaca credential is either empty or invalid. Please enter below to access"
                     " the account information."
        }
    else:
        userdata = {
            'name': user.first_name,
            'alpaca_id': alpaca_id,
            'alpaca_key': " " + "*" * 10,
            'total_equity': user_details['equity'],
            'buy_power': user_details['buy_power'],
            'portfolio': user_details['display_portfolio'],
            'cash': user_details['cash'],
            'tradable_cash': user_details['usable_cash'],
            'currency': user_details['currency'],
            'short_portfolio_value': user_details['short_portfolio_value'],
            'long_portfolio_value': user_details['long_portfolio_value'],
            'orders': user_details['orders'],
            'strategy': user_details['strategy'],
            'percent_change': user_details['portfolio_percent_change'],
            'dollar_change': user_details['portfolio_dollar_change'],
            # change direction is used to determine if the price is going positive or negative
            'change_direction': user_details['portfolio_change_direction']
        }
    return user, userdata, auth0user, user_details


@login_required
def dashboard(request):
    user, userdata, auth0user, user_details = get_user_information(request)
    # managing forms
    from backend.auth0login.forms import CredentialForm, OrderForm, StrategyForm
    credential_form = CredentialForm(request.POST or None)
    order_form = OrderForm(request.POST or None)
    strategy_form = StrategyForm(request.POST or None)
    if request.method == 'POST':
        # let user input their Alpaca API information
        if 'submit_credential' in request.POST:
            if credential_form.is_valid():
                if hasattr(user, 'credential'):
                    user.credential.alpaca_id = credential_form.get_id()
                    user.credential.alpaca_key = credential_form.get_key()
                    user.credential.save()
                else:
                    from .models import Credential
                    cred = Credential(user=request.user, alpaca_id=credential_form.get_id(),
                                      alpaca_key=credential_form.get_key())
                    cred.save()
                return HttpResponseRedirect('/')

        if 'submit_order' in request.POST:
            if order_form.is_valid():
                response = order_form.place_order(user, user_details)
                order_form = OrderForm()
                #  update order for display
                from backend.tradingbot.models import Order
                userdata["orders"] = [order.display_order() for order in
                                      Order.objects.filter(user=user).order_by('-timestamp').iterator()]
                return render(request, 'home/index.html', {
                    'credential_form': credential_form,
                    'order_form': order_form,
                    'strategy_form': StrategyForm(None),
                    'auth0User': auth0user,
                    'userdata': userdata,
                    'order_submit_form_response': response,
                })

        if 'submit_strategy' in request.POST:
            if strategy_form.is_valid():
                # here for some reason form.cleaned_data changed from type dict to
                # type tuple. I tried to find the reason but it didn't seem to caused by
                # our code. Might be and django bug
                strategy = strategy_form.cleaned_data
                user.portfolio.strategy = strategy
                user.portfolio.save()
                return HttpResponseRedirect('/')

    graph = get_portfolio_chart(request)
    return render(request, 'home/index.html', {
        'credential_form': credential_form,
        'order_form': order_form,
        'strategy_form': strategy_form,
        'auth0User': auth0user,
        'userdata': userdata,
        'stock_graph': graph
    })


@login_required()
def get_portfolio_chart(request):
    user, userdata, auth0user, user_details = get_user_information(request)

    if user_details is None:
        return
    API_KEY = user.credential.alpaca_id
    API_SECRET = user.credential.alpaca_key
    BASE_URL = "https://paper-api.alpaca.markets"
    alpaca = api.REST(key_id=API_KEY, secret_key=API_SECRET,
                    base_url=BASE_URL, api_version='v2')

    portfolio_hist = alpaca.get_portfolio_history().df
    portfolio_hist = portfolio_hist.reset_index()
    line_plot = px.line(portfolio_hist, "timestamp", "equity")
    line_plot.update_layout(
        xaxis_title="",
        yaxis_title="Equity"
    )

    line_plot = line_plot.to_html()
    return line_plot


@login_required
def get_stock_chart(request, symbol):
    user, userdata, auth0user, user_details = get_user_information(request)

    API_KEY = user.credential.alpaca_id
    API_SECRET = user.credential.alpaca_key
    alpaca = api.REST(API_KEY, API_SECRET)
    # Setting parameters before calling method
    timeframe = "1Day"
    start = "2021-01-01"
    today = date.today()
    yesterday = today - timedelta(days=1)
    end = "2021-02-01"
    # Retrieve daily bars for SPY in a dataframe and printing the first 5 rows
    spy_bars = alpaca.get_bars(symbol, timeframe, start, end).df
    candlestick_fig = go.Figure(
        data=[go.Candlestick(x=spy_bars.index, open=spy_bars['open'],
                             high=spy_bars['high'], low=spy_bars['low'], close=spy_bars['close'])])
    candlestick_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price ($USD)")
    candlestick_fig = candlestick_fig.to_html()
    return candlestick_fig


@login_required
def orders(request):
    user, userdata, auth0user, user_details = get_user_information(request)
    # managing forms
    from backend.auth0login.forms import CredentialForm, OrderForm, StrategyForm
    credential_form = CredentialForm(request.POST or None)
    order_form = OrderForm(request.POST or None)
    strategy_form = StrategyForm(request.POST or None)
    if request.method == 'POST':
        if 'submit_credential' in request.POST:
            if credential_form.is_valid():
                if hasattr(user, 'credential'):
                    user.credential.alpaca_id = credential_form.get_id()
                    user.credential.alpaca_key = credential_form.get_key()
                    user.credential.save()
                else:
                    from .models import Credential
                    cred = Credential(user=request.user, alpaca_id=credential_form.get_id(),
                                      alpaca_key=credential_form.get_key())
                    cred.save()
                return HttpResponseRedirect('/')

        if 'submit_order' in request.POST:
            if order_form.is_valid():
                response = order_form.place_order(user, user_details)
                order_form = OrderForm()
                #  update order for display
                from backend.tradingbot.models import Order
                userdata["orders"] = [order.display_order() for order in
                                      Order.objects.filter(user=user).order_by('-timestamp').iterator()]
                return render(request, 'home/index.html', {
                    'credential_form': credential_form,
                    'order_form': order_form,
                    'strategy_form': StrategyForm(None),
                    'auth0User': auth0user,
                    'userdata': userdata,
                    'order_submit_form_response': response,
                })

        if 'submit_strategy' in request.POST:
            if strategy_form.is_valid():
                # here for some reason form.cleaned_data changed from type dict to
                # type tuple. I tried to find the reason but it didn't seem to caused by
                # our code. Might be and django bug
                rebalance_strategy = strategy_form.cleaned_data[0]
                optimization_strategy = strategy_form.cleaned_data[1]
                user.portfolio.rebalancing_strategy = rebalance_strategy
                user.portfolio.optimization_strategy = optimization_strategy
                user.portfolio.save()
                return HttpResponseRedirect('/')
    return render(request, 'home/orders.html', {
        'credential_form': credential_form,
        'order_form': order_form,
        'strategy_form': strategy_form,
        'auth0User': auth0user,
        'userdata': userdata,
    })


@login_required
def positions(request):
    from backend.auth0login.forms import WatchListForm, StrategyForm
    user, userdata, auth0user, user_details = get_user_information(request)
    watchlist_form = WatchListForm(request.POST or None)
    strategy_form = StrategyForm(request.POST or None)
    if request.method == 'POST':
        if 'add_to_watchlist' in request.POST:
            if watchlist_form.is_valid():
                response = watchlist_form.add_to_watchlist(user)
                return render(request, 'home/positions.html', {
                    'watchlist_form': watchlist_form,
                    'strategy_form': strategy_form,
                    'watchlist_form_response': response,
                    'auth0User': auth0user,
                    'userdata': userdata,
                })

        if 'submit_strategy' in request.POST:
            if strategy_form.is_valid():
                # here for some reason form.cleaned_data changed from type dict to
                # type tuple. I tried to find the reason but it didn't seem to caused by
                # our code. Might be and django bug
                strategy = strategy_form.cleaned_data
                user.portfolio.strategy = strategy
                user.portfolio.save()
                return HttpResponseRedirect('positions')

    return render(request, 'home/positions.html', {
        'watchlist_form': watchlist_form,
        'strategy_form': strategy_form,
        'auth0User': auth0user,
        'userdata': userdata,
    })


@login_required
def user_settings(request):
    return render(request, 'home/page-not-implemented.html')  # 'home/user-settings.html')


@login_required
def machine_learning(request):
    return render(request, 'home/page-not-implemented.html')  # 'home/machine-learning.html')


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)
