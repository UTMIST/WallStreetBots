import numpy as np
import pandas as pd
from backend.settings import BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY
from .portfoliomanager import PortfolioManager


class NaiveHMMPortfolioUpdate(PortfolioManager):
    def __init__(self, portfolio, data_fetcher, HMMdatafetcher, start, end, HMM, num_hidden_states, covar_type, n_iter, buffer=0.05):
        """
        Args:
            portfolio: portfolio dictionary contains cash and stocks with qty
            data_fetcher: source of stock data
            buffer: proportion of the portfolio to be cash (buffer zone for price fluctuations)
        """
        super(NaiveHMMPortfolioUpdate, self).__init__(portfolio, None)
        self.total_portfolio_value = None
        self.price_dict = None
        self.data_fetcher = data_fetcher
        self.buffer = buffer
        self.start = start
        self.end = end
        self.HMMdatafetcher = HMMdatafetcher
        self.HMM = HMM
        self.num_hidden_states, self.covar_type, self.n_iter = num_hidden_states, covar_type, n_iter
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
        buy_list = []
        new_portfolio = {}
        for i in self.portfolio_stocks.keys():
            datamanager = self.HMMdatafetcher(BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY, i, self.start, self.end)
            current_data = datamanager.align_data('all')
            current_hmm = self.HMM(current_data, self.num_hidden_states, self.covar_type, self.n_iter)
            current_hmm.train(current_data)
            current_hmm.evaluation()
            current_hmm.inference()

            if current_hmm.num_uptrend == 1:  # stock price goes up
                buy_list.append(i)

        for stock in buy_list:
            qty = (self.total_portfolio_value * (1 - self.buffer) / len(buy_list)) / self.price_dict[stock]
            qty = round(qty, 2)
            new_portfolio[stock] = qty

        return new_portfolio
