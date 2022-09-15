import numpy as np


def Nop():
    return np.nan


class Transaction:
    def __init__(self, currency, amount, fraction=False):
        assert amount >= 0, "Amount must be non-negative"
        assert (not fraction) or (amount <= 1), "Fraction to transact can't be above 1"
        self.currency = currency
        self.amount = amount
        self.fraction = fraction

    def __repr__():
        pass


class Buy(Transaction):
    def __init__(self, currency, amount, fraction=False):
        super().__init__(currency, amount, fraction)

    def __repr__(self):
        if self.fraction:
            return f"Buy {self.amount * 100:.0f}% of cash holdings worth of {self.currency}"
        else:
            return f"Buy {self.amount} of {self.currency}"


class Sell(Transaction):
    def __init__(self, currency, amount, fraction=False):
        super().__init__(currency, amount, fraction)

    def __repr__(self):
        if self.fraction:
            return f"Sell {self.amount * 100:.0f}% of cash holdings worth of {self.currency}"
        else:
            return f"Sell {self.amount} of {self.currency}"
