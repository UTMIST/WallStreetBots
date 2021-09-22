from django.db import models


class Bar(models.Model):
    bar_symbol = models.CharField(max_length=10)
    time = models.DateTimeField('Beginning time of this bar')
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.IntegerField()
