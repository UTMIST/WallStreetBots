import datetime
from datetime import timedelta

from alpaca_trade_api.rest import TimeFrame

from backend.tradingbot.apimanagers import AlpacaManager


class DataFetcher:
    """
    generic stock data fetcher
    """

    def get_cur_price(self, *args, **kwargs):
        return 0

    def get_past_price(self, *args, **kwargs):
        return 0

    def get_today_news(self, *args, **kwargs):
        return {"headline": "this is the headline"}


class AlpacaFetcher(DataFetcher):
    """
    wrapper around Alpaca API
    """
    TIMESTEP = {"MINUTE": TimeFrame.Minute, "HOUR": TimeFrame.Hour, "DAY": TimeFrame.Day}

    def __init__(self, AlpacaID, AlpacaKey):
        super().__init__()
        self.api = AlpacaManager(AlpacaID, AlpacaKey)
        self.api.validate_api()

    def get_cur_price(self, ticker):
        """
        note that I wrapped around get_bar instead of get_price because I
        want to make sure the price is adjusted
        """
        start = (datetime.datetime.now(datetime.timezone.utc) - timedelta(days=1)).isoformat()
        end = datetime.datetime.now(datetime.timezone.utc).isoformat()
        prices, _ = self.api.get_bar(ticker, TimeFrame.Minute, start, end)
        return prices[0]

    def get_past_price(self, ticker, timestep, start, end, price_type='close', adjustment='all'):
        timestep = self.TIMESTEP[timestep]
        prices, times = self.api.get_bar(ticker, timestep, start, end, price_type=price_type, adjustment=adjustment)
        # prices and times from latest to oldest
        return prices, times


class DummyFetcher(DataFetcher):
    def get_past_price(self, *args, **kwargs):
        return [102, 103, 102, 101, 100, 99], ['t6', 't5', 't4', 't3', 't2', 't1']

    def get_cur_price(self, *args, **kwargs):
        return 102
