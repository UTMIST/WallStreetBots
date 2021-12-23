import requests, json
import alpaca_trade_api as tradeapi


class APImanager():  # API manager for Alpaca
    def __init__(self, API_KEY, SECRET_KEY):
        self.BASE_URL = "https://paper-api.alpaca.markets"
        self.ACCOUNT_URL = "{}/v2/account".format(self.BASE_URL)
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.api = tradeapi.REST(API_KEY, SECRET_KEY, self.BASE_URL, api_version='v2')

    def get_bar(self, symbol, timestep, start, end, price_type="close"):
        """
        Get a list of prices from latest to oldest with a timestep

        Args:
          symbol: the name of the stock
          timestep: TimeFrame.Day, TimeFrame.Hour, TimeFrame.Minute
          start: Starting time, RFC-3339 format
          end:Ending time, RFC-3339 format
          price_type: open, close, high, low

        Returns:
          - a list of prices from latest to oldest with a timestep
          - a list of time associated with each price
        """
        try:
            bars = self.api.get_bars(symbol, timestep, start, end, adjustment='raw').df
            if bars.empty:
                return [], []
            # print(bars)
            bar_t = list(bars.index)[::-1]
            bar_prices = bars[price_type].tolist()[::-1]  # bars is price data in time step from latest to oldest
            return bar_prices, [t.to_pydatetime() for t in bar_t]
        except Exception as e:
            return "Failed to get bars from Alpaca: " + str(e)

    def get_price(self, symbol):
        """
        Get get the current price of a stock

        Args:
          symbol: the name of the stock

        Returns:
          an float of the current price of the stock

        Note now the current price is based on last trade
        """
        try:
            bar = self.api.get_last_trade(symbol)
            price = bar._raw['price']
            return price
        except Exception as e:
            return "Failed to get price from Alpaca: " + str(e)

    def market_close(self):
        """
        checks if market closes

        Args:
          t: the time to check if the market is closed
          if no argument is passed, check if the market is currently open or closed

        Returns:
          True / False

        To be completed
        """
        api = tradeapi.REST()
        clock = api.get_clock()

        if clock.is_open:
            return True
        else:
            return False



    def get_account(self):
        """
        Get the account using the URL and the API_KEY

        Args:
          N/A

        Returns:
          the account in the format of a json string
        """
        try:
            r = requests.get(self.ACCOUNT_URL, headers={'APCA-API-KEY-ID': self.API_KEY, 'APCA-API-SECRET-KEY': self.SECRET_KEY})
            account = json.loads(r.content)
            return account
        except Exception as e:
            return "Failed to accesss account: " + str(e)

    def market_buy(self, symbol, qty):
        """
        Buy the stocks specificied

        Args:
          Strock Symbol (String)
          Quantity (int)

        Returns:

        """
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            log = 'Success to market buy'
        except Exception as e:
            log = 'Failed to market buy: ' + str(e)
        return log

    def market_sell(self, symbol, qty):
        """
        Sell the stock specified

        Args:
          Strock Symbol (String)
          Quantity (int)

        Returns:
          N/A

        """
        try:
            self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
            log = 'Success to market sell'
        except Exception as e:
            log = 'Failed to market sell: ' + str(e)
        return log
