from django.db import models
from django.contrib.auth.models import User

ALPACA_ID_MAX_LENGTH = 100
ALPACA_KEY_MAX_LENGTH = 100


class Credential(models.Model):
    """stores the user's Alpaca API key and secret key"""

    # Fields
    user = models.OneToOneField(User, help_text='Associated user', on_delete=models.CASCADE)
    alpaca_id = models.CharField(max_length=ALPACA_ID_MAX_LENGTH, help_text='Enter your Alpaca id')
    alpaca_key = models.CharField(max_length=ALPACA_KEY_MAX_LENGTH, help_text='Enter your Alpaca key')

    # Metadata
    class Meta:
        ordering = ['user']

    #Methods
    def __str__(self):
        return "Credential for " + str(self.user)
