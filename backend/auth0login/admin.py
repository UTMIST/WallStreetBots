from django.contrib import admin
from .models import Credential, Order, Portfolio, BotInstance, StockInstance


class CredentialAdmin(admin.ModelAdmin):
    list_display = ('user', 'alpaca_id', 'alpaca_key')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'order_type', 'price', 'quantity')


# Register your models here.
admin.site.register(Credential, CredentialAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Portfolio)
admin.site.register(BotInstance)
admin.site.register(StockInstance)

