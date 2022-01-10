class StocksManagerNaive:

    def __init__(self, bots, account):
        self.bots = bots
        self.account_balance, self.portfolio = self.extract_acc_info(account)

    def make_decision(self):
        '''
        Creates a dictionary of stock name as key and number of stock to buy or sell as values,
        based on the decisions of the bots.
        Note postive number denotes buying and negative number denotes selling
        '''
        action_dict = {}  # e.g. {"APPL": 10}

        for bot in self.bots:
            decision = bot.make_decision()
            balance = bot.balance
            share_price = bot.stock.cur_price
            symbol = bot.stock.symbol
            if decision == 'buy':
                n_shares = int(balance / share_price)
                if n_shares != 0:
                    if symbol in action_dict.keys():
                        action_dict[symbol] = action_dict[symbol] + n_shares
                    else:
                        action_dict[symbol] = n_shares
                    bot.balance = balance - n_shares * share_price
                    bot.shares = n_shares

                    print("-> buying", symbol, "for", n_shares, "shares for $", share_price, "per share")

            elif decision == 'sell':
                if bot.shares != 0:
                    if symbol in action_dict.keys():
                        action_dict[symbol] = action_dict[symbol] + -1 * bot.shares
                    else:
                        action_dict[symbol] = -1 * bot.shares
                    bot.balance += bot.shares * share_price
                    bot.shares = 0

                    print("-> Selling", int(-1 * action_dict[symbol]), "for", bot.shares, "shares for $", share_price,
                          "per share")

        if action_dict == {}:
            print("--- No action performed at this time ---")
        return action_dict

    def extract_acc_info(self, account):
        '''
        This function needs to be implemented
        '''
        # put extract stuff here
        account_balance, portfolio = None, None
        return account_balance, portfolio
