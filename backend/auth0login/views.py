from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect(dashboard)
    else:
        return render(request, 'login.html')


@login_required
def dashboard(request):
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
            'alpaca_key': "*"*len(alpaca_key),
            'total_equity': user_details['equity'],
            'buy_power': user_details['buy_power'],
            'portfolio': user_details['portfolio'],
        }

    # let user input their Alpaca API information
    from backend.auth0login.forms import CredentialForm
    form = CredentialForm(request.POST or None)
    if form.is_valid():
        if hasattr(user, 'credential'):
            user.credential.alpaca_id = form.get_id()
            user.credential.alpaca_key = form.get_key()
            user.credential.save()
        else:
            from .models import Credential
            cred = Credential(user=request.user, alpaca_id=form.get_id(), alpaca_key=form.get_key())
            cred.save()
        return HttpResponseRedirect('/')

    return render(request, 'dashboard.html', {
        'form': form,
        'auth0User': auth0user,
        'userdata': userdata
    })


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)


def sync_alpaca(user):
    """
        sync user related database data with Alpaca
        this is a simplified, incomplete version.
    """
    user_details = {}
    # check if user has credential
    if not hasattr(user, 'credential'):
        return

    from backend.tradingbot.apimanagers import APImanager
    api = APImanager(user.credential.alpaca_id, user.credential.alpaca_key)

    # check if api is valid
    if not api.validate_api()[0]:
        print(api.validate_api()[1])
        return

    # get account information
    account = api.get_account()
    user_details['equity'] = account.equity
    user_details['buy_power'] = account.buying_power

    # get portfolio information
    portfolio = api.get_positions()
    for position in portfolio:
        print("{} shares of {}".format(position.qty, position.symbol))

    # non-user specific synchronization. e.g. add new company, new stock if it didn't exist
    from backend.tradingbot.models import Company, Stock
    for position in portfolio:
        if not Company.objects.filter(ticker=position.symbol).exists():
            # add Company
            company = Company(name=position.symbol, ticker=position.symbol)
            company.save()
            # add Stock
            stock = Stock(company=company)
            stock.save()
            print(f"added {position.symbol} to Company and Stock")

    print(account)
    # user-specific synchronization
    # 1) check if user has a portfolio
    """
    if not hasattr(user, 'portfolio'):
        from .models import Portfolio
        port = Portfolio(user=user, cash=, name='default-1')
        port.save()
    """
    # 2) update portfolio cash
    # 3) check if user has stock instance
    # for position in portfolio:
    #


    user_details['portfolio'] = portfolio
    return user_details
