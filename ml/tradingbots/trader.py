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


class Strategy:
    def __init__(self, name):
        self.name = name

    def get_actions(self, portfolio):
        return []


class MonteCarloMAShapeRatioStrategy(Strategy):
    def get_actions(self, portfolio):
        """
        Args:
            portfolio:   dict in the form {SYMB1:QTY, SYMB2:QTY}

        Returns:
            actions:    list of action objects
        """
        # from pipelines import

        actions = []
        return actions

## use django.setup to access database
