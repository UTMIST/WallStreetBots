from http import HTTPStatus

import alpaca_trade_api as tradeapi
import alpaca_trade_api.common


class AlpacaManager():  # API manager for Alpaca
    def __init__(self, API_KEY, SECRET_KEY):
        self.BASE_URL = alpaca_trade_api.common.URL("https://paper-api.alpaca.markets")
        self.ACCOUNT_URL = "{}/v2/account".format(self.BASE_URL)
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        if self.validate_api()[0]:
            self.api = tradeapi.REST(API_KEY, SECRET_KEY, self.BASE_URL, api_version='v2')

    def validate_api(self):
        """
        Test if the API ID/Key pair is valid
        """
        try:
            self.api = tradeapi.REST(self.API_KEY, self.SECRET_KEY, self.BASE_URL, api_version='v2')
            self.api.get_account()
            return True, "api id/key pair validated"
        except Exception as e:
            return False, str(e)

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
            return True, price
        except Exception as e:
            return False, "Failed to get price from Alpaca: " + str(e)

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
        try:
            clock = self.api.get_clock()
            if clock.is_open:
                return True
            else:
                return False
        except Exception as e:
            return "Failed to check market status from Alpaca " + str(e)

    def get_account(self):
        """
        Get the account using the URL and the API_KEY

        Args:
          N/A

        Returns:
          the account in the format of a json string
        """
        try:
            return self.api.get_account()
        except Exception as e:
            return "Failed to access account: " + str(e)

    def get_positions(self):
        """
        Get the account using the URL and the API_KEY

        Args:
          N/A

        Returns:
          the account in the format of a json string
        """
        try:
            return self.api.list_positions()
        except Exception as e:
            return "Failed to access portfolio: " + str(e)

    def market_buy(self, symbol, qty, client_order_id=None):
        """
        Buy the stocks specified

        Args:
          symbol (String)
          qty (int)

        Returns:

        """
        if client_order_id is not None:
            res = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='gtc',
                client_order_id=client_order_id
            )
        else:
            res = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        if res.status == HTTPStatus.FORBIDDEN:
            print("Insufficient funds")
            return False
        if res.status == HTTPStatus.UNPROCESSABLE_ENTITY:
            print("Malformed request")
            return False
        return True

    def market_sell(self, symbol, qty, client_order_id=None):
        """
        Sell the stock specified

        Args:
          symbol (String)
          qty (int)

        Returns:
          N/A

        """
        if client_order_id is not None:
            res = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='gtc',
                client_order_id=client_order_id
            )
        else:
            res = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
        if res.status == HTTPStatus.FORBIDDEN:
            print("Insufficient quantity")
            return False
        if res.status == HTTPStatus.UNPROCESSABLE_ENTITY:
            print("Malformed request")
            return False
        return True
