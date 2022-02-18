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

    def __init__(self, order_type, transaction_type, ticker, quantity):
        self.order_type = order_type
        self.transaction_type = transaction_type
        self.ticker = ticker
        self.quantity = quantity


class Strategy:
    def __init__(self, name):
        self.name = name

    def get_actions(self, portfolio):
        return []


class MonteCarloMAShapeRatioStrategy(Strategy):
    def get_actions(self, portfolio):
        # from pipelines import
        actions = []
