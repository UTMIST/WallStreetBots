from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler


def create_portfolio_dictionary(portfolio):
    from .models import StockInstance
    result = {'cash': float(portfolio.cash)}
    stock_instances = StockInstance.objects.filter(portfolio=portfolio)
    result['stocks'] = []
    for stock_instances in stock_instances:
        result['stocks'].append(stock_instances.stock.company.ticker)
    return result


def start_pipelines():
    from django.contrib.auth.models import User
    from ml.tradingbots.pipelines.monte_carlo_w_ma import MonteCarloMovingAveragePipline
    rebalancing_strategies = {"monte_carlo": MonteCarloMovingAveragePipline}
    pipelines = []
    for user in User.objects.all():
        if user.portfolio:
            rebalancing_strategy = rebalancing_strategies[user.portfolio.rebalancing_strategy]
            pipelines.append(rebalancing_strategy("MonteCarlo", create_portfolio_dictionary(user.portfolio)))

    for pipeline in pipelines:
        pipeline.rebalance()


class TradingbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.tradingbot'

    def ready(self):
        scheduler = BackgroundScheduler()
        # TODO: change this interval from 5 seconds to something more reasonable
        # currently 5 seconds to make it easy to check that it is working
        scheduler.add_job(start_pipelines, 'interval', seconds=5)
        scheduler.start()
