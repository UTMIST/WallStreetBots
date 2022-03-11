from django.apps import AppConfig


class TradingbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.tradingbot'

    def create_portfolio_dictionary(self, portfolio):
        # import django
        # django.setup()
        from .models import StockInstance
        result = {'cash': float(portfolio.cash)}
        stock_instances = StockInstance.objects.filter(portfolio=portfolio)
        result['stocks'] = []
        for stock_instances in stock_instances:
            result['stocks'].append(stock_instances.stock.company.ticker)
        return result

    def ready(self):
        from django.contrib.auth.models import User
        from ml.tradingbots.pipelines.monte_carlo_w_ma import MonteCarloMovingAveragePipline
        pipelines = []
        for user in User.objects.all():
            if user.portfolio:
                pipelines.append(MonteCarloMovingAveragePipline("MonteCarlo", self.create_portfolio_dictionary(user.portfolio)))

        for pipeline in pipelines:
            pipeline.rebalance()
