class PortfolioManager:
    def __init__(self, portfolio, metric):
        self.portfolio_cash = portfolio["cash"]
        self.portfolio_stocks = portfolio["stocks"]
        self.metric = metric

    def rebalance(self):
        return self.portfolio_stocks
