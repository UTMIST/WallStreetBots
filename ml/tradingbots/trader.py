class Action:
    """
    data class returned by Strategy class

    ORDERTYPES = [
        ('M', 'Market'),
        ('L', 'Limit'),
        ('S', 'Stop'),
        ('ST', 'Stop Limit'),
        ('T', 'Trailing Stop'),
    ]
    TRANSACTIONTYPES = [
        ('B', 'Buy'),
        ('S', 'Sell'),
    ]
    """
    ORDERTYPES = ['M', 'L', 'S', 'ST', 'T', ]
    TRANSACTIONTYPES = ['B', 'S', ]

    def __init__(self, order_type, transaction_type, ticker, quantity):
        self.order_type = order_type
        assert order_type in Action.ORDERTYPES
        self.transaction_type = transaction_type
        assert transaction_type in Action.TRANSACTIONTYPES
        self.ticker = ticker
        self.quantity = quantity

    def __dict__(self):
        return {'order_type': self.order_type,
                'transaction_type': self.transaction_type,
                'ticker': self.ticker,
                'quantity': self.quantity
                }


class Strategy:
    def __init__(self, name):
        self.name = name

    def get_actions(self, portfolio):
        return []


class MonteCarloMAShapeRatioStrategy(Strategy):
    def get_actions(self, portfolio):
        """
        Args:
            portfolio:   dict in the form {cash: QTY, stocks: {SYMB1:QTY, SYMB2:QTY}}

        Returns:
            actions:    list of action objects
        """
        from pipelines.monte_carlo_w_ma import MonteCarloMovingAveragePipline
        pipeline = MonteCarloMovingAveragePipline(name=self.name, portfolio=portfolio)
        actions = pipeline.rebalance(order_type='M')
        return actions

#  use django.setup to access database
