from django.urls import path

from . import views

# TODO: add route for creating, patching company
urlpatterns = [
    path('', views.index, name='tradingbot_welcome'),
    path('stock_trade', views.StockTradeView.as_view(), name='stock_trade'),
]
