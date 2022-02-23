class DataFetcher:
    """
    generic stock data fetcher
    """

    def get_cur_price(self, ticker):
        return 0

    def get_past_price(self, ticker, timestep, start, end, price_type='close', adjustment='all'):
        return 0

    def get_today_news(self):
        return {"headline": "this is the headline"}


class AlpacaFetcher(DataFetcher):
    """
    wrapper around Alpaca API
    """

    def __init__(self, AlpacaID, AlpacaKey):
        super().__init__()
