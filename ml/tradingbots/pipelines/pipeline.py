from ..trader import Action


class Pipeline:
    def __init__(self, name, portfolio):
        self.name = name
        self.portfolio_cash = portfolio["cash"]
        self.portfolio_stocks = portfolio["stocks"]

    def __str__(self):
        return self.name

    def pipeline(self):
        """
        This method is to be implemented in the subclasses
        Should return a new portfolio_stocks
        """
        return self.portfolio_stocks

    def calc_actions(self, order_type='M'):
        """
        generate a list of actions based on the change in portfolio
        Args:
            order_type: string

        Returns:
            actions: list of action objects
        """

        # run the pipline and get the portfolio before and after
        PreP, PostP = self.portfolio_stocks, self.pipeline()

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

    def rebalance(self, order_type='M'):
        """
        call this method to get the rebalanced portfolio
        by default, it is expected to override the pipeline method, and the orders
        are default market orders.

        If the trading strategy uses other way to generate Actions instead of based on
        the change in portfolio, override the calc_actions function.
        """
        return self.calc_actions(order_type=order_type)
