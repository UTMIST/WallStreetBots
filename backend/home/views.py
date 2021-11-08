from django.http import HttpResponse
from django.db import connection


def index(request):
    return HttpResponse("Hello World, welcome to homepage of UTMIST's tradingbot! Checkout /tradingbot as well")


def get_time(request):
    cursor = connection.cursor()
    cursor.execute('''select date_trunc('minute', now())''')
    current_datetime = cursor.fetchone()[0]
    return HttpResponse(f"{current_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
