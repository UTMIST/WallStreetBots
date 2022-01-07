from django.contrib.auth.models import User
from django.db import models

from backend.tradingbot.models import Portfolio


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


class BotInstance(models.Model):
    """An instance of a bot"""
    name = models.CharField(max_length=100, blank=False, help_text="Bot Name")
    portfolio = models.OneToOneField(Portfolio, blank=True, help_text='Associated portfolio', on_delete=models.CASCADE)
    user = models.ForeignKey(User, help_text='Associated user', on_delete=models.CASCADE)
    bot = None  # To Be Completed

    # Metadata
    class Meta:
        ordering = ['user']

    # Methods
    def __str__(self):
        return f'Bot: {self.name} \n User: {str(self.user)} \n' \
               f' Portfolio: {self.portfolio.name}'
