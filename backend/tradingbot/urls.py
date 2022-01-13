from django.urls import path

from . import views

# TODO: add route for creating, patching company
urlpatterns = [
    path('', views.index, name='tradingbot_welcome'),
    path('stock_trade', views.stock_trade, name='stock_trade'),
]
