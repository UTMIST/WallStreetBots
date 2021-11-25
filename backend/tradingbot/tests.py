from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Company, StockTrade


class TradingbotTests(APITestCase):

    def setUp(self) -> None:
        company = Company(
            name="Apple",
            ticker="AAPL",
        )
        company.save()

        StockTrade.objects.create(
            company=company,
            price=100,
            amount=100,
        )

    def test_chatbot_welcome(self):
        url = reverse("tradingbot_welcome")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_trade_argument(self):
        url = reverse("stock_trade")
        response = self.client.post(url, {"trade": "option"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_trade(self):
        url = reverse("stock_trade")
        response = self.client.post(
            url,
            {"transaction_type": "buy", "ticker": "AAPL", "amount": "1", "price": "100"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StockTrade.objects.all().count(), 2)

    def test_invalid_buy(self):
        url = reverse("stock_trade")
        response = self.client.post(
            url,
            {"transaction_type": "invalid_options", "ticker": "AAPL", "amount": "1", "price": "100"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIsInstance(response.json()["data"], type(None))

    def test_trade_get(self):
        url = reverse("stock_trade")
        random_trade = StockTrade.objects.all()[0]
        response = self.client.get(url, {"id": random_trade.id})
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["price"], random_trade.price)
        self.assertEqual(json_response["company_id"], random_trade.company.id)
