from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler


def create_portfolio_dictionary(portfolio):
    from .models import StockInstance
    result = {'cash': float(portfolio.cash)}
    stock_instances = StockInstance.objects.filter(portfolio=portfolio)
    result['stocks'] = {}
    for stock_instances in stock_instances:
        result['stocks'][stock_instances.stock.company.ticker] = float(stock_instances.quantity)
    return result

    # {
    #   cash: float,
    #   stocks: {
    #       ticker: qty
    #   }
    # }


def start_pipelines():
    from django.contrib.auth.models import User
    from ml.tradingbots.pipelines.monte_carlo_w_ma import MonteCarloMovingAveragePipline
    from ml.tradingbots.trader import MonteCarloMASharpeRatioStrategy
    rebalancing_strategies = {
        "monte_carlo": MonteCarloMASharpeRatioStrategy,
        "hmm": None
    }
    pipelines = []
    users_to_actions = {}
    for user in User.objects.all():
        if user.portfolio:
            strat = MonteCarloMASharpeRatioStrategy("Name")
            actions = strat.get_actions(create_portfolio_dictionary(user.portfolio))
            users_to_actions[user.username] = actions
    for user, actions in users_to_actions.items():
        for action in actions:
            # TODO: place order based on action
            pass


class TradingbotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.tradingbot'

    def ready(self):
        scheduler = BackgroundScheduler()
        # TODO: change this interval from 5 seconds to something more reasonable
        # currently 5 seconds to make it easy to check that it is working
        scheduler.add_job(start_pipelines, 'interval', seconds=60*60*24)
        scheduler.start()
