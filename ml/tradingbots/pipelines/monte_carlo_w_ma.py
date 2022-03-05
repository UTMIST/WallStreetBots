from backend.settings import BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY
from pipeline import Pipeline
from ..components.metrics import MovingAverageSharpeRatio
from ..components.montecarlo import MonteCarloPortfolioUpdate
from ..components.utils import AlpacaFetcher


class MonteCarloMovingAveragePipline(Pipeline):
    def pipeline(self):
        fetcher = AlpacaFetcher(BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY)
        past_days, max_n, timestep, rf = 3, 300, 'DAY', 0.02
        metric = MovingAverageSharpeRatio(self.portfolio_stocks, past_days, max_n, timestep, rf, fetcher)
        metric.configure()
        manager = MonteCarloPortfolioUpdate(self.portfolio, metric, fetcher, simulation_itr=10000, buffer=0.05)
        return manager.rebalance()
