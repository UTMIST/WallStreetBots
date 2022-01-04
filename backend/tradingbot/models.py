from django.db import models
from rest_framework import serializers


class News(models.Model):
    """News of a company"""
    headline = models.TextField()
    link = models.URLField(max_length=200)  # default = 200
    date = models.DateField(auto_now=False, auto_now_add=False)

    # Metadata
    class Meta:
        ordering = ['date']

    # Methods
    def __str__(self):
        return f'Healine: {str(self.headline)} \n Link: {self.link} \n Date: {self.date}'


class Tweets(models.Model):
    """Tweets/Reddits of a compay"""
    content = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=False)

    # Metadata
    class Meta:
        ordering = ['date']

    # Methods
    def __str__(self):
        return f'Content: {str(self.content)} \n Date: {self.date}'


class Company(models.Model):
    """Company entity"""
    name = models.TextField()
    ticker = models.BigAutoField(primary_key=True)
    news = models.ManyToManyField(News)
    tweets = models.ManyToManyField(Tweets)

    # Metadata
    class Meta:
        ordering = ['ticker']

    # Methods
    def __str__(self):
        return f'Name: {str(self.name)} \n Ticker: {self.ticker}'


class Stock(models.Model):
    """Stock of a company"""
    company = models.OneToOneField(Company, help_text='Company', on_delete=models.CASCADE)  # To Be Completed
    current_price = None  # To Be Completed
    indicators = None  # To Be Completed
    Historical_prices = None  # To Be Completed
    Historical_volatility = None  # To Be Completed

    # Metadata
    class Meta:
        ordering = ['company']

    # Methods
    def __str__(self):
        return None  # To Be Completed


class Price(models.Model):
    """Price of a stock"""
    stock = models.ForeignKey(Stock, help_text='Associated stock', on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    value = models.DecimalField(max_digits=8, decimal_places=2, help_text='quantity')

    # Metadata
    class Meta:
        ordering = ['date']

    # Methods
    def __str__(self):
        return f'Stock: {str(self.stock.company)} \n Date: {self.date} \n Value: {self.value}'


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
