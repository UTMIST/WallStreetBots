import numpy as np
import matplotlib.pyplot as plt
import math

class Account:
  def __init__(self, acc_dict):
    self.acc_dict = acc_dict

class Stock:
  
  def __init__(self, symbol, cur_price, t, bar_list, timeframe, closing_t):
    '''
    symbol: string, symbol of the stock. e.g. "APPL"
    cur_price: float, current price. e.g. 125.48
    t: daytime object, current time. 
    bar_list: return from the api call containing past prices
    timeframe: string, timeframe between each price. e.g. day / hour / minute
    closing_t: time object, closing time of the latest price in bar_list
    '''

    self.symbol = symbol
    self.past_price = self.past_price_from_bars(bar_list) # past closing prices ranges from latest to oldest
    self.timeframe = timeframe
    self.cur_price = cur_price
    self.time = t
    self.closing_t = closing_t

  def past_price_from_bars(self, bar_list):
    # right now assume bar_list is just a list of numbers
    return np.array(bar_list)

  def moving_average(self, start, past_pts = 10):
    assert (start + past_pts) < self.past_price.size, "past price index out of range"
    return np.sum(self.past_price[start:(start+past_pts)]) / past_pts

  def update(self, cur_price, bar, bar_t, t):
    '''
    update the status of the stock

    args:
    cur_price: float, current price. e.g. 125.48
    bar: list, list of closing prices with time step of self.timeframe. latest is the first element
    bar_t: list, list of daytime object associated to each element of bar (in order). latest is the first element
    t: daytime object, current time.

    returns:
    None
    '''
    #print("------")
    #print(bar, bar_t)
    self.cur_price = cur_price
    self.time = t
    if bar == [] or bar_t == []:
        return
    if self.closing_t < bar_t[-1]:
        self.past_price = np.insert(self.past_price, 0, bar[-1])
        self.closing_t = bar_t[-1]
        self.update(cur_price, bar[:-1], bar_t[:-1],t)
    elif self.closing_t >= bar_t[-1]:
        self.update(cur_price, bar[:-1], bar_t[:-1],t)

  def macd(self, cur, arr):
    return self.EMA(12, cur, arr) - self.EMA(26, cur, arr)

  def EMA(self, N, cur, arr):
    k = 2/(N+1)
    EMA = arr[N-1]
    #a vectorized version would be better
    for i in range(N-2, -1, -1):
      EMA = arr[i] * k + EMA * (1-k)
    EMA = cur * k + EMA * (1-k)
    return EMA

  def ccvol(self, start, days, arr):    
    sum_vol = 0
    var_days = []
    var = 0;
    for i in range(days):
      if (i+start) != 0:       
        var_days.append(math.log(arr[i+start]/arr[start+i-1]))
        sum_vol += math.log(arr[start+i]/arr[start+i-1])     
    for v in var_days:
      var += (v - (sum_vol / days)) ** 2
    var /= days
    return math.sqrt(var) * math.sqrt(252)
  

  def plot_price(self, past_pts = 15):

      ma_prices10 = [self.moving_average(i) for i in range(0, past_pts)] [::-1]
      ema_prices12 = [self.EMA(12, price, self.past_price[i+1:]) for i, price in enumerate(np.insert(self.past_price, 0, self.cur_price)[:past_pts])] [::-1]
      ma_prices5 = [self.moving_average(i, 5) for i in range(0, past_pts)] [::-1]
      ema_prices26 = [self.EMA(26, price, self.past_price[i+1:]) for i, price in enumerate(np.insert(self.past_price, 0, self.cur_price)[:past_pts])] [::-1]
      plt.clf()
      prices = self.past_price[::-1]
      prices = np.append(prices, self.cur_price)
      plt.plot(range(past_pts), prices[-past_pts:], label = "prices")
      #plt.plot(range(past_pts), ma_prices5, label = "5 pts moving average")
      #plt.plot(range(past_pts), ma_prices10, label = "10 pts moving average")
      plt.plot(range(past_pts), ema_prices12, label = "12 pts exponential moving average")
      plt.plot(range(past_pts), ema_prices26, label = "26 pts exponential moving average")
      plt.title(self.symbol + " Prices")
      plt.legend()
      plt.xlabel(str(self.timeframe))
      plt.ylabel("Price ($)")  
      plt.show()