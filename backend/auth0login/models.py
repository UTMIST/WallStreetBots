from django.db import models
from django.contrib.auth.models import User


class Credential(models.Model):
    """stores the user's Alpaca API key and secret key"""
    ALPACA_ID_MAX_LENGTH = 100
    ALPACA_KEY_MAX_LENGTH = 100
    # Fields
    user = models.OneToOneField(User, help_text='Associated user', on_delete=models.CASCADE)
    alpaca_id = models.CharField(max_length=ALPACA_ID_MAX_LENGTH, help_text='Enter your Alpaca id')
    alpaca_key = models.CharField(max_length=ALPACA_KEY_MAX_LENGTH, help_text='Enter your Alpaca key')

    # Metadata
    class Meta:
        ordering = ['user']

    # Methods
    def __str__(self):
        return "Credential for " + str(self.user)


class Order(models.Model):
    """Historical orders for user"""
    ORDERTYPES = [
        ('MB', 'Market buy'),
        ('MS', 'Market sell'),
        ('LB', 'Limit buy'),
        ('LS', 'Limit sell'),
        ('SB', 'Stop buy'),
        ('SS', 'Stop sell'),
    ]
    # Fields
    order_number = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, help_text='Associated user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, help_text='order timestamp')
    # company = None  # leave empty for now
    order_type = models.CharField(choices=ORDERTYPES, max_length=2, help_text='order type')
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text='order price')
    quantity = models.DecimalField(max_digits=8, decimal_places=2, help_text='quantity')

    # Metadata
    class Meta:
        ordering = ['user', 'timestamp', 'order_type']

    # Methods
    def __str__(self):
        return f"Order {self.order_number} \n User: {self.user} \n" \
               f"Timestamp: {self.timestamp} \n Company: {str(self.company)}" \
               f"Order type: {self.order_type} \n Price: {self.price} \n Quantity: {self.quantity}"


class Portfolio(models.Model):
    """Portfolio for a user"""
    name = models.CharField(max_length=100, blank=False, help_text="Portfolio name")
    user = models.ForeignKey(User, help_text='Associated user', on_delete=models.CASCADE)

    # Metadata
    class Meta:
        ordering = ['user']

    # Methods
    def __str__(self):
        return f'Portfolio: {self.name} \n User: {str(self.user)}'


class BotInstance(models.Model):
    """An instance of a bot"""
    name = models.CharField(max_length=100, blank=False, help_text="Bot Name")
    portfolio = models.OneToOneField(Portfolio, blank = True,help_text='Associated portfolio', on_delete=models.CASCADE)
    user = models.ForeignKey(User, help_text='Associated user', on_delete=models.CASCADE)
    # bot = None  # To Be Completed

    # Metadata
    class Meta:
        ordering = ['user']

    # Methods
    def __str__(self):
        return f'Bot: {self.name} \n User: {str(self.user)} \n' \
               f' Portfolio: {self.portfolio.name}'


class StockInstance(models.Model):
    """An instance of a stock"""
    portfolio = models.ForeignKey(Portfolio, help_text='Associated portfolio', on_delete=models.CASCADE)
    # stock = None  # To Be Completed
    quantity = models.DecimalField(max_digits=8, decimal_places=2, help_text='quantity')

    # Metadata
    class Meta:
        ordering = ['portfolio']

    # Methods
    def __str__(self):
        return f'Stock: {str(self.stock)} \n Quantity: {self.quantity} \n Portfolio: {self.portfolio.name}'
