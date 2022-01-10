from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from backend.tradingbot.synchronization import sync_alpaca


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
            'alpaca_key': "*" * len(alpaca_key),
            'total_equity': user_details['equity'],
            'buy_power': user_details['buy_power'],
            'portfolio': user_details['portfolio'],
            'cash': user_details['cash'],
            'tradable_cash': user_details['usable_cash'],
            'currency': user_details['currency'],
            'short_portfolio_value': user_details['short_portfolio_value'],
            'long_portfolio_value': user_details['long_portfolio_value'],
            'orders': user_details['orders'],
        }
    # managing forms
    from backend.auth0login.forms import CredentialForm, OrderForm
    credential_form = CredentialForm(request.POST or None)
    order_form = OrderForm(request.POST or None)
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
                return render(request, 'dashboard.html', {
                    'credential_form': credential_form,
                    'order_form': order_form,
                    'auth0User': auth0user,
                    'userdata': userdata,
                    'order_submit_form_response': response,
                })

    return render(request, 'dashboard.html', {
        'credential_form': credential_form,
        'order_form': order_form,
        'auth0User': auth0user,
        'userdata': userdata,
    })


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)
