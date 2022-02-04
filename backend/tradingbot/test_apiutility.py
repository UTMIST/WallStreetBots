from django.test import TestCase
from unittest.mock import MagicMock
from .apimanagers import AlpacaManager
from django.contrib.auth.models import User
from .models import Order

from .apiutility import place_general_order


class TestApiUtilities(TestCase):
    def setUp(self):
        self.api_manager = AlpacaManager("test", "test")

    def test_place_general_order(self):
        self.api_manager.validate_api = MagicMock(return_value=True)
        self.api_manager.get_price = MagicMock(return_value=(True, 100))
        self.api_manager.api.submit_order = MagicMock(return_value=True)

        user = User.objects.create_user(username="test", password="test")
        user_details = {
            "usable_cash": 100,
        }
        result = place_general_order(
            user,
            user_details,
            "test_ticker",
            1,
            "B",
            "M",
            "time_in_force",
            self.api_manager
        )
        self.assertTrue(result)
        num_orders = Order.objects.filter(user=user).count()
        self.assertTrue(num_orders == 1)
