import unittest
from utils import DummyFetcher
from metrics import DummyMetric
from montecarlo import MonteCarloPortfolioUpdate
import numpy as np


class MonteCarloPortfolioUpdateTestCase(unittest.TestCase):
    portfolio = {'cash': 1000,
                 'stocks': {"AAPL": 3, "MSFT": 2}
                 }
    data_fetcher = DummyFetcher()
    metric = DummyMetric()

    def test_initialization(self):
        test_manager = MonteCarloPortfolioUpdate(self.portfolio, self.metric, self.data_fetcher, simulation_itr=2)
        self.assertEqual(test_manager.total_portfolio_value, 1510)
        self.assertEqual(list(test_manager.price_dict.keys()), ["AAPL", "MSFT"])
        self.assertEqual(list(test_manager.price_dict.values()), [102, 102])

    def test_rebalance(self):
        self.assertEqual(True, True)  # add assertion here
        np.random.seed(69)
        test_manager = MonteCarloPortfolioUpdate(self.portfolio, self.metric, self.data_fetcher, simulation_itr=2)
        PostP = test_manager.rebalance()
        self.assertEqual(PostP, {'AAPL': 3.77, 'MSFT': 10.29})


if __name__ == '__main__':
    unittest.main()
