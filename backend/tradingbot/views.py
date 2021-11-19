from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework import status

from .models import StockTrade, StockTradeSerializer, Company


def index(request):
    return HttpResponse("Hello World, welcome to tradingbot!")


class StockTradeView(View):
    model = StockTrade

    def get(self, request):
        id = request.GET.get('id')
        user_message = self.model.objects.get(id=id)
        return JsonResponse(StockTradeSerializer(user_message).data)

    def post(self, request):
        transaction_type = request.POST.get('transaction_type')
        if transaction_type == 'sell':
            self.sell_stock(request)
        if transaction_type == 'buy':
            self.buy_stock(request)

        return HttpResponse(
            {"data": "the only supported transactions are 'buy' or 'sell'"},
            status=status.HTTP_400_BAD_REQUEST
        )

    def sell_stock(self, request):
        return HttpResponse(status=status.HTTP_501_NOT_IMPLEMENTED)

    def buy_stock(self, request):
        ticker = request.POST.get('ticker').lower()
        price = float(request.POST.get('price'))
        amount = int(request.POST.get('amount'))
        company = Company.objects.get(ticker=ticker)
        self.model.objects.create(company=company, price=price, amount=amount)
        return HttpResponse(status=status.HTTP_201_CREATED)
