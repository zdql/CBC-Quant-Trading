from operator import inv
import numpy as np
import pandas as pd
from transactions import Buy, Sell, Nop
import time


class PortfolioManager:
    def __init__(self, starting_cash):
        self.data = pd.DataFrame([])
        self.starting_cash = starting_cash
        self.cash = starting_cash
        self.investments = {}
        self.strategies = np.array([])
        # add transactions
        self.Buy = Buy
        self.Sell = Sell
        self.Nop = Nop

    # add variants parameter to allow many different versions of the line to exist in the PM object
    def link_data(self, name, data):
        self.data = pd.concat([self.data, data.rename(name)], axis=1)
        self.investments[name] = 0

    def add_strategy(self, strategy):
        self.strategies = np.append(self.strategies, [strategy])

    def reset(self):
        self.cash = self.starting_cash
        self.strategies = np.array([])
        for currency in self.investments:
            self.investments[currency] = 0

    def execute_transaction(self, tx, time):
        if isinstance(tx, Buy):
            currency_price = self.data[tx.currency][time]
            if tx.fraction:
                tx_amt_usd = tx.amount * self.cash
            else:
                tx_amt_usd = min(currency_price * tx_amt, self.cash)
            tx_amt = tx_amt_usd / currency_price

            self.cash -= tx_amt_usd
            self.investments[tx.currency] += tx_amt

        elif isinstance(tx, Sell):
            currency_price = self.data[tx.currency][time]
            if tx.fraction:
                tx_amt = tx.amount * self.investments[tx.currency]
            else:
                tx_amt = min(tx.amount, self.investments[tx.currency])
            tx_amt_usd = tx_amt * currency_price

            self.investments[tx.currency] -= tx_amt
            self.cash += tx_amt_usd

        elif tx is Nop():
            pass

    @classmethod
    def get_time(cls):
        return time.time()

    def run(self):
        strat_orders = []
        for strategy in self.strategies:
            strat_orders.append(strategy(self.data))
        orderbook = pd.concat(strat_orders, axis=1).sort_index()

        orderbook = orderbook[~orderbook.isna().all(axis=1)]
        for time, orders in orderbook.iterrows():
            for order in orders:
                self.execute_transaction(order, time)

    def portfolio_value(self):
        total_cash = self.cash
        for currency, amount in self.investments.items():
            total_cash += amount * self.data[currency].ffill().iloc[-1]
        return total_cash

    def summarize(self):
        print(f"Start Value: ${self.starting_cash:.2f}")
        print(f"End Value: ${self.portfolio_value():.2f}")
