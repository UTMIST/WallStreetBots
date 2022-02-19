from django.apps import AppConfig


class TradingbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.tradingbot'
    verbose_name = 'Trading Bot'

    def ready(self):
        from .portfolio_balancing import task_runner
        task_runner()
