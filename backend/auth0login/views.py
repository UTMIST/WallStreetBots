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
    auth0user = user.social_auth.get(provider='auth0')
    alpaca_id = user.credential.alpaca_id if hasattr(user, 'credential') else "no alpaca id"
    alpaca_key = user.credential.alpaca_key if hasattr(user, 'credential') else "no alpaca key"
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'Alpaca id': alpaca_id,
        'Alpaca Secret key': alpaca_key,
        'email': auth0user.extra_data['email'],
    }
    from backend.auth0login.forms import CredentialForm
    form = CredentialForm(request.POST or None)

    if form.is_valid():
        if hasattr(user, 'credential'):
            user.credential.alpaca_id = form.get_id()
            user.credential.alpaca_key = form.get_key()
        else:
            from .models import Credential
            cred = Credential(user=request.user, alpaca_id=form.get_id(), alpaca_key=form.get_key())
            cred.save()

    return render(request, 'dashboard.html', {
        'form': form,
        'auth0User': auth0user,
        'userdata': userdata  # json.dumps(userdata, indent=4)
    })


def logout(request):
    log_out(request)
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    return HttpResponseRedirect(logout_url)
