import unittest
from .utils import DummyFetcher
from ..components.naiveportfoliomanager import NaiveHMMPortfolioUpdate


class DummyHMM:
    def __init__(self, current_data, num_hidden_states, covar_type, n_iter, **kwargs):
        self.stock = current_data.stock
        if self.stock == "AAPL" or self.stock == "MSFT":
            self.num_uptrend = 1
        else:
            self.num_uptrend = 0
        return

    def train(self, current_data, **kwargs):
        return

    def evaluation(self, **kwargs):
        return

    def inference(self, **kwargs):
        return


class DummyHMM_fetcher:
    class DummyData:
        def __init__(self, stock):
            self.stock = stock

    def __init__(self, BACKEND_ALPACA_ID, BACKEND_ALPACA_KEY, i, start, end, **kwargs):
        self.stock = i
        return

    def align_data(self, config):
        return self.DummyData(self.stock)


class MonteCarloPortfolioUpdateTestCase(unittest.TestCase):
    portfolio = {'cash': 1000,
                 'stocks': {"AAPL": 3, "MSFT": 2, "TSLA": 4}
                 }
    data_fetcher = DummyFetcher()
    HMM = DummyHMM
    DataManager = DummyHMM_fetcher

    def test_initialization(self):
        buffer = 0.05
        start = None
        end = None
        num_hidden_states, covar_type, n_iter = None, None, None
        NHPU = NaiveHMMPortfolioUpdate(self.portfolio, self.data_fetcher, self.DataManager,
                                       start, end, self.HMM, num_hidden_states, covar_type, n_iter, buffer=buffer)
        self.assertEqual(NHPU.total_portfolio_value, 1918)
        self.assertEqual(list(NHPU.price_dict.keys()), ["AAPL", "MSFT", "TSLA"])
        self.assertEqual(list(NHPU.price_dict.values()), [102, 102, 102])

    def test_rebalance(self):
        buffer = 0.05
        start = None
        end = None
        num_hidden_states, covar_type, n_iter = None, None, None
        NHPU = NaiveHMMPortfolioUpdate(self.portfolio, self.data_fetcher, self.DataManager, start, end, self.HMM,
                                       num_hidden_states,
                                       covar_type, n_iter, buffer=buffer)
        PostP = NHPU.rebalance()
        self.assertEqual(PostP, {'AAPL': 8.93, 'MSFT': 8.93})


if __name__ == '__main__':
    unittest.main()
