# Generated by Django 3.2.8 on 2022-01-11 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tradingbot', '0006_auto_20220110_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='optimization_strategy',
            field=models.CharField(choices=[('none', 'None'), ('ma_sharp_ratio', 'Sharp ratio based on moving average')], default='none', help_text='Optimization Strategy', max_length=50),
        ),
    ]
