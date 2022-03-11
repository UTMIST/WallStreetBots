import unittest
import metrics
from utils import DummyFetcher


class MovingAverageSharpeRatioTestCase(unittest.TestCase):
    def test_sharpe_ratio(self):
        """
        test on:
        AAPL        MSFT
        99          99
        100         100
        101         101
        102         102
        103         103
        102         102

        weight = [0.7, 0.3]
        """
        stocks = ["AAPL", "MSFT"]
        fetcher = DummyFetcher()
        test_metric = metrics.MovingAverageSharpeRatio(stocks, past_days=10, max_n=5, timestep="DAY",
                                                       rf=0.02, fetcher=fetcher)
        # print(test_metric.generate_stock_returns())
        # print(test_metric.generate_stock_returns().pct_change())
        test_metric.configure()
        # print(test_metric.cov)
        # print(test_metric.n_points)
        sharpe = test_metric.apply([0.3, 0.7])
        # print(sharpe)
        self.assertEqual(round(sharpe, 3), 0.228)  # add assertion here


if __name__ == '__main__':
    unittest.main()
