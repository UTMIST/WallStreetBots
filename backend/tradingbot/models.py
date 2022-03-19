from django.contrib.auth.models import User
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
        return f'Headline: {str(self.headline)} \n Link: {self.link} \n Date: {self.date}'


class Tweets(models.Model):
    """Tweets/Reddits of a company"""
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
    ticker = models.CharField(max_length=255, primary_key=True)
    news = models.ManyToManyField(News, blank=True)
    tweets = models.ManyToManyField(Tweets, blank=True)

    # Metadata
    class Meta:
        ordering = ['ticker']

    # Methods
    def __str__(self):
        return f'{self.ticker}'


class Stock(models.Model):
    """Stock of a company"""
    company = models.OneToOneField(Company, help_text='Company', on_delete=models.CASCADE)  # To Be Completed
    current_price = None  # To Be Completed
    indicators = None  # To Be Completed
    historical_prices = None  # To Be Completed
    historical_volatility = None  # To Be Completed

    # Metadata
    class Meta:
        ordering = ['company']

    # Methods
    def __str__(self):
        return str(self.company)  # To Be Completed


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
    # should probably change to represent a single exchange instance instead of trying to
    # show an entire buy/sell operation
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.FloatField()
    amount = models.IntegerField()
    bought_timestamp = models.DateTimeField(auto_now_add=True)
    sold_timestamp = models.DateTimeField(null=True)


class StockTradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTrade
        fields = ('company_id', 'price', 'amount', 'bought_timestamp', 'sold_timestamp')


class Order(models.Model):
    """Historical orders for user"""
    ORDERTYPES = [
        ('M', 'Market'),
        ('L', 'Limit'),
        ('S', 'Stop'),
        ('ST', 'Stop Limit'),
        ('T', 'Trailing Stop'),
    ]
    TRANSACTIONTYPES = [
        ('B', 'Buy'),
        ('S', 'Sell'),
    ]
    STATUS = [
        ('A', 'Accepted'),
        ('F', 'Filled'),
        ('N', 'New'),
        ('C', 'Closed')
    ]
    # Fields
    order_number = models.BigAutoField(primary_key=True)
    client_order_id = models.CharField(max_length=100, default='', help_text='for alpaca sync')
    user = models.ForeignKey(User, help_text='associated user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, help_text='order submission timestamp')
    stock = models.ForeignKey(Stock, help_text='associated stock', on_delete=models.CASCADE)
    order_type = models.CharField(choices=ORDERTYPES, max_length=2, help_text='order type')
    quantity = models.DecimalField(max_digits=8, decimal_places=2, help_text='quantity')
    transaction_type = models.CharField(choices=TRANSACTIONTYPES, max_length=2,
                                        help_text='buy or sell transaction type')
    status = models.CharField(choices=STATUS, max_length=1, help_text='order status')

    # Not required
    filled_avg_price = models.DecimalField(max_digits=8, decimal_places=2, help_text='filled average price', blank=True,
                                           null=True)
    filled_timestamp = models.DateTimeField(blank=True, help_text='order filled timestamp', null=True)
    limit_price = models.DecimalField(max_digits=8, decimal_places=2, help_text='limit price', blank=True, null=True)
    stop_price = models.DecimalField(max_digits=8, decimal_places=2, help_text='stop price', blank=True, null=True)
    filled_quantity = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text='filled quantity')

    # Metadata
    class Meta:
        ordering = ['user', 'timestamp', 'order_type']

    # Methods
    def __str__(self):
        return f"Order {self.order_number} \n User: {self.user} \n" \
               f"Timestamp: {self.timestamp} \n Company: {str(self.stock)}" \
               f"Order type: {self.order_type} \n Price: {self.filled_avg_price} \n Quantity: {self.quantity}"

    def display_order(self):
        ret = {
            'stock': str(self.stock),
            'quantity': str(self.quantity),
            'type': f'{mapping(str(self.order_type), Order.ORDERTYPES)} '
                    f'{mapping(str(self.transaction_type), Order.TRANSACTIONTYPES)}',
            'timestamp': str(self.timestamp),
            'filled_quantity': str(self.filled_quantity),
            'filled_avg_price': str(self.filled_avg_price),
            'status': mapping(str(self.status), Order.STATUS),
        }
        return ret


def mapping(key, choices):
    for row in choices:
        if row[0] == key:
            return row[1]


class Portfolio(models.Model):
    BALANCINGSTRATEGY = [
        ('manual', 'Manual portfolio management'),
        ('monte_carlo', 'Monte carlo portfolio rebalancing'),
    ]
    OPTIMIZATIONSTRATEGY = [
        ('none', 'None'),
        ('ma_sharp_ratio', 'Sharpe ratio based on moving average'),
    ]
    """Portfolio for a user"""
    name = models.CharField(max_length=100, blank=False, help_text="Portfolio name")
    user = models.OneToOneField(User, help_text='Associated user', on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=10, decimal_places=2, help_text='Cash')
    rebalancing_strategy = models.CharField(max_length=50, choices=BALANCINGSTRATEGY, default='manual',
                                            help_text="Portfolio Rebalancing Strategy")
    optimization_strategy = models.CharField(max_length=50, choices=OPTIMIZATIONSTRATEGY,
                                             default='none', help_text='Optimization Strategy')

    # Metadata
    class Meta:
        ordering = ['user']

    # Methods
    def __str__(self):
        return f'Portfolio: {self.name} \n User: {str(self.user)}'


class StockInstance(models.Model):
    """An instance of a stock"""
    user = models.ForeignKey(User, help_text='Associated user', on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, help_text='Associated portfolio', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, help_text='Associated stock', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, help_text='quantity')

    # Metadata
    class Meta:
        ordering = ['user', 'portfolio']

    # Methods
    def __str__(self):
        return f'User: {str(self.user)} Stock: {str(self.stock)} \n Quantity: {self.quantity} \n ' \
               f'Portfolio: {self.portfolio.name}'
