from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework import status

from .models import StockTrade, StockTradeSerializer, Company


def index(request):
    # ALPACA SECRET KEY
    return HttpResponse("Hello World, welcome to tradingbot!")


class StockTradeView(View):
    # TODO: Add alpaca integration
    model = StockTrade

    def get(self, request):
        id = request.GET.get("id")
        stock_trade = self.model.objects.all().filter(id=id).first()
        return JsonResponse(StockTradeSerializer(stock_trade).data, safe=False)

    def post(self, request):
        transaction_type = request.POST.get("transaction_type")
        if transaction_type == "sell":
            return HttpResponse(status=status.HTTP_501_NOT_IMPLEMENTED)

        if transaction_type == "buy":
            ticker = request.POST.get("ticker")
            price = float(request.POST.get("price"))
            amount = int(request.POST.get("amount"))
            company = Company.objects.filter(ticker=ticker).first()
            if not company:
                return JsonResponse(
                    {"data": f"ticker: {ticker} not valid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.model.objects.create(company=company, price=price, amount=amount)
            return HttpResponse(status=status.HTTP_201_CREATED)


        return JsonResponse(
            {"data": "the only supported transactions are 'buy' or 'sell'"},
            status=status.HTTP_400_BAD_REQUEST
        )
