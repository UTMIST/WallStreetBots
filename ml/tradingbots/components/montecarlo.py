import numpy as np
import pandas as pd

from .portfoliomanager import PortfolioManager


class MonteCarloPortfolioUpdate(PortfolioManager):
    def __init__(self, portfolio, metric, data_fetcher, simulation_itr=10000, buffer=0.05):
        """
        Args:
            portfolio: portfolio dictionary contains cash and stocks with qty
            metric: metric object, the metric which the portfolio algorithm optimizes on
            data_fetcher: source of stock data
            simulation_itr: number of simulation iterations for monte carlo
            buffer: proportion of the portfolio to be cash (buffer zone for price fluctuations)
        """
        super(MonteCarloPortfolioUpdate, self).__init__(portfolio, metric)
        self.total_portfolio_value = None
        self.price_dict = None
        self.simulation_itr = simulation_itr
        self.data_fetcher = data_fetcher
        self.buffer = buffer
        self.utils()

    def utils(self):
        stocks = self.portfolio_stocks.keys()
        # fetch current price for all stocks
        price_dict = {}
        total_portfolio_value = self.portfolio_cash
        for ticker in stocks:
            price_dict[ticker] = self.data_fetcher.get_cur_price(ticker)
            total_portfolio_value += price_dict[ticker] * self.portfolio_stocks[ticker]
        self.price_dict = price_dict
        self.total_portfolio_value = total_portfolio_value

    def rebalance(self):
        """
        call this method to rebalance the portfolio
        """
        stocks = self.portfolio_stocks.keys()
        portfolios = pd.DataFrame(columns=[*stocks, "Sharpe Ratio"])

        for i in range(self.simulation_itr):
            weights = np.random.random(len(stocks))
            weights /= np.sum(weights)
            portfolios.loc[i, stocks] = weights
            portfolios.loc[i, "Sharpe Ratio"] = self.metric.apply(weights)
        # get the maximum sharpe ratio
        best = portfolios[portfolios["Sharpe Ratio"] == portfolios["Sharpe Ratio"].max()]
        # convert to stock qty dict and return
        PostP = {}
        for ticker in stocks:
            w = float(best.loc[:, ticker])
            qty = w * self.total_portfolio_value * (1 - self.buffer) / self.price_dict[ticker]
            PostP[ticker] = round(qty, 2)
        return PostP
