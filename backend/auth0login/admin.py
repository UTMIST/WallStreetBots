from django.contrib import admin
from .models import Credential, BotInstance
from ..tradingbot.models import Order, Portfolio, StockInstance


class CredentialAdmin(admin.ModelAdmin):
    list_display = ('user', 'alpaca_id', 'alpaca_key')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'order_type', 'filled_avg_price', 'quantity')


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'cash')


class BotInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'portfolio', 'user', 'bot')


class StockInstanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'portfolio', 'stock', 'quantity')



# Register your models here.
admin.site.register(Credential, CredentialAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(BotInstance, BotInstanceAdmin)
admin.site.register(StockInstance, StockInstanceAdmin)
