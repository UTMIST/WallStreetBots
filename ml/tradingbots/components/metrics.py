import numpy as np
import pandas as pd


class Metric:
    def configure(self, *args, **kwargs):
        return 0

    def apply(self, *args, **kwargs):
        return 0


class MovingAverageSharpeRatio(Metric):
    def __init__(self, stocks, past_days, max_n, timestep, rf, fetcher):
        """
        Args:
            stocks: list, list of stock tickers
            past_days: int, number of past days consider
            timestep: string, "MINUTE", "HOUR" or "DAY"
            max_n: int, maximum number of past data points to consider
            rf: float, Returns of a Risk-free Investment
        """
        self.stocks = stocks
        self.past_days = past_days
        self.max_n = max_n
        self.timestep = timestep
        self.rf = rf
        self.fetcher = fetcher
        self.returns = None
        self.cov = None
        self.n_points = None

    def generate_stock_returns(self):
        all_prices = pd.DataFrame()
        import datetime
        from datetime import timedelta
        start = (datetime.datetime.now(datetime.timezone.utc) - timedelta(days=self.past_days)).isoformat()
        end = datetime.datetime.now(datetime.timezone.utc).isoformat()
        for stock in self.stocks:
            prices, _ = self.fetcher.get_past_price(stock, self.timestep, start, end)
            prices = prices[:self.max_n][::-1] if self.max_n < len(prices) else prices[::-1]
            all_prices.loc[:, stock] = prices
        return all_prices

    def configure(self):
        """
        one time configuration of the covariance matrix
        """
        prices = self.generate_stock_returns()
        self.n_points = len(prices)
        returns = prices.pct_change()
        cov = returns.cov()
        self.returns = returns
        self.cov = cov

    def apply(self, weights):
        """
        computes the sharpe ratio based on the portfolio weights
        Args:
            weights: 1D np.array() with weights of each stock
        """
        # rp = (self.returns.mean() * 252) @ weights
        # port_var = weights @ (self.cov * 252) @ weights
        rp = (self.returns.mean() * self.n_points) @ weights
        port_var = weights @ (self.cov * self.n_points) @ weights
        sharpe = (rp - self.rf) / np.sqrt(port_var)
        return sharpe
