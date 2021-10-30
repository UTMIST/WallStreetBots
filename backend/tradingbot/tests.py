from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class TradingbotTests(APITestCase):

    def test_chatbot_welcome(self):
        url = reverse("tradingbot_welcome")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

