from django.db import models
from rest_framework import serializers


class Company(models.Model):
    name = models.TextField()
    ticker = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return f"{self.name}:{self.ticker}"


class StockTrade(models.Model):
    # TODO: this is an overly simplistic model.
    # need to add things like bought_price, sold_price, etc.
    # or add transaction type (buy, sell, etc.) which is probably preferable
    # should probably change to represent a single exchange instance instead of trying to show an entire buy/sell operation
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.FloatField()
    amount = models.IntegerField()
    bought_timestamp = models.DateTimeField(auto_now_add=True)
    sold_timestamp = models.DateTimeField(null=True)


class StockTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTrade
        fields = ('company_id', 'price', 'amount', 'bought_timestamp', 'sold_timestamp')
