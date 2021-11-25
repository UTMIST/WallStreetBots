import requests, json
import alpaca_trade_api as tradeapi
import pandas as pd
from alpaca_trade_api.rest import TimeFrame


BASE_URL = "https://paper-api.alpaca.markets"
ACCOUNT_URL = "{}/v2/account".format(BASE_URL)

def market_close(t):
  '''
  checks if market closes

  Args:
    t: the time to check if the market is closed

  Returns:
    True / False

  To be completed
  '''
  return True # always return true for now


class APImanager(): # API manager for Alpaca
  def __init__(self, API_KEY, SECRET_KEY):
      self.API_KEY = API_KEY
      self.SECRET_KEY = SECRET_KEY
      self.api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

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
      bars = self.api.get_bars(symbol, timestep, start, end, adjustment='raw').df
      if bars.empty:
          return [],[]
      #print(bars)
      bar_t = list(bars.index)[::-1]
      bar_prices = bars[price_type].tolist()[::-1] # bars is price data in time step from latest to oldest
      return bar_prices, [t.to_pydatetime() for t in bar_t]

  def get_price(self, symbol):
      """
      Get get the current price of a stock
      
      Args:
        symbol: the name of the stock
      
      Returns:
        an float of the current price of the stock

      Note now the current price is based on last trade
      """
      #ur_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
      bar = self.api.get_last_trade(symbol)
      price = bar._raw['price']

      return price

  def get_account(self):
      """
      Get the account using the URL and the API_KEY
      
      Args:
        N/A
      
      Returns:
        the account in the format of a json string 
      """
      r = requests.get(ACCOUNT_URL, headers =   {'APCA-API-KEY-ID': self.API_KEY, 'APCA-API-SECRET-KEY': self.SECRET_KEY})
      account = json.loads(r.content)
      return account
  
  

  def buy_stocks(self, symbol, qty):
      """
      Buy the stocks specificied
      
      Args:
        Strock Symbol (String)
        Quantity (int)
      
      Returns:
        
      """
      self.api.submit_order(
      symbol = symbol,
      qty= qty,
      side= 'buy',
      type='market',
      time_in_force='gtc'
      )
      
  

  def sell_stocks(self, symbol, qty):
    """
    Sell the stock specified 
    
    Args:
      Strock Symbol (String)
      Quantity (int)
    
    Returns:
      N/A
      
    """
    self.api.submit_order(
    symbol = symbol,
    qty= qty,
    side= 'sell',
    type='market',
    time_in_force='gtc'
    )                                                          

#debugs 
#manager = APImanager(API_KEY, SECRET_KEY)
#print(manager.get_account())
#manager.buy_stocks("APPL", 5)