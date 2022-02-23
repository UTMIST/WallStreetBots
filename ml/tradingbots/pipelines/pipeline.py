from ..trader import Action


class Pipeline:
    def __init__(self, name, portfolio):
        self.name = name
        self.portfolio = portfolio

    def __str__(self):
        return self.name

    def pipeline(self):
        """
        This method is to be implemented in the subclasses
        Should return a new portfolio
        """
        return self.portfolio

    def calc_actions(self, order_type='M'):
        """
        generate a list of actions based on the change in portfolio
        Args:
            PreP: portfolio dictionary before balancing in the form {SYMB1:QTY, SYMB2:QTY}
            PostP: portfolio dictionary after balancing in the form {SYMB1:QTY, SYMB2:QTY}
            order_type: string

        Returns:
            actions: list of action objects
        """

        PreP, PostP = self.portfolio, self.pipeline()

        def get_transaction_type(qty):
            if qty < 0:
                return "S"
            elif qty > 0:
                return "B"
            return False

        def get_action(key):
            qty1 = PreP[key] if key in PreP.keys() else 0
            qty2 = PostP[key] if key in PostP.keys() else 0
            qty = qty2 - qty1
            if get_transaction_type(qty):
                return Action(order_type=order_type, transaction_type=get_transaction_type(qty), ticker=key,
                              quantity=qty)
            else:
                return False

        tickers = set().union(*[PreP, PostP])  # get all tickers
        return [get_action(key) for key in tickers]

    def rebalance(self):
        return self.calc_actions(order_type='M')
