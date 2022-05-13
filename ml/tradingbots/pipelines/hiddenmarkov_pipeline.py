from backend.settings import BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY
from pipeline import Pipeline
from ..components.hiddenmarkov import DataManager
from ..components.hiddenmarkov import HMM
import datetime
from datetime import timedelta
from ..components.utils import AlpacaFetcher


class HMMPipline(Pipeline):
    def utils(self):
        stocks = self.portfolio_stocks.keys()
        fetcher = AlpacaFetcher(BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY)
        # fetch current price for all stocks
        price_dict = {}
        total_portfolio_value = self.portfolio_cash
        for ticker in stocks:
            price_dict[ticker] = fetcher.get_cur_price(ticker)
            total_portfolio_value += price_dict[ticker] * self.portfolio_stocks[ticker]
        self.price_dict = price_dict
        self.total_portfolio_value = total_portfolio_value

    def pipeline(self):
        # fetcher = AlpacaFetcher(BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY) # need this?
        buffer = 0.05
        start = (datetime.datetime.now(datetime.timezone.utc) - timedelta(days=1)).isoformat()
        end = datetime.datetime.now(datetime.timezone.utc).isoformat()
        num_hidden_states, covar_type, n_iter = 10, 'full', 100
        self.utils()
        buy_list = []
        new_portfolio = {}
        for i in self.portfolio_stocks.keys():
            current_data = DataManager(BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY, i, start, end)
            current_hmm = HMM(current_data, num_hidden_states, covar_type, n_iter)
            current_hmm.train(current_data)
            current_hmm.evaluation()
            current_hmm.inference()

            # not sure
            if current_hmm.num_uptrend == 1: # stock price goes up
                buy_list.append(i)

        for stock in buy_list:
            qty =(self.total_portfolio_value * (1-buffer) / len(buy_list))/self.price_dict[stock]
            qty = round(qty, 2)
            new_portfolio[stock] = qty

        return new_portfolio