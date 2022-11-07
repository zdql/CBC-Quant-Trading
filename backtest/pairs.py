import pandas as pd
import numpy as np
from pm import PortfolioManager
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

pm = PortfolioManager(1000)

btc_close = pd.read_csv("../data/BTC/USD.csv", index_col="time").close
eth_close = pd.read_csv("../data/ETH/USD.csv", index_col="time").close

df = pd.concat([btc_close, eth_close], axis=1, ignore_index=False)
df = df[~df.isna().any(axis=1)]
df = df.iloc[-40000:]

btc_close = df.iloc[:, 0]
eth_close = df.iloc[:, 1]

pm.link_data("btc", btc_close)
pm.link_data("eth", eth_close)

# score, pvalue, _ = coint(btc_close, eth_close)
# print(score, pvalue)

btc_close = sm.add_constant(btc_close)
results = sm.OLS(eth_close, btc_close).fit()
btc_close = btc_close["close"]
b = results.params["close"]
const = results.params["const"]

spread = eth_close - b * btc_close - const
mean = spread.mean()
std = spread.std()
normalized_spread = (spread - mean) / std
plt.plot(normalized_spread)
plt.axhline(0, color="black")
plt.axhline(1, color="red")
plt.axhline(-1, color="red")
plt.show()


def btc_strat(data):
    spread = data["eth"] - b * data["btc"] - const
    normalized_spread = (spread - mean) / std

    # buy
    below_neg_1 = (normalized_spread < -1) & (normalized_spread.shift() > -1)
    # sell
    above_1 = (normalized_spread > 1) & (normalized_spread.shift() < 1)
    # buy if 1 to -1, sell if -1 to 1
    sell = np.sign(normalized_spread).diff() / 2
    sell[0] = 0

    orders = below_neg_1.astype(int) - above_1.astype(int) - sell.astype(int)
    return orders.map(
        lambda x: pm.Sell("btc", 1, fraction=True)
        if x == 1
        else pm.Buy("btc", 1, fraction=True)
        if x == -1
        else pm.Nop()
    )


def eth_strat(data):
    spread = data["eth"] - b * data["btc"] - const
    normalized_spread = (spread - mean) / std

    # buy
    below_neg_1 = (normalized_spread < -1) & (normalized_spread.shift() > -1)
    # sell
    above_1 = (normalized_spread > 1) & (normalized_spread.shift() < 1)
    # buy if 1 to -1, sell if -1 to 1
    sell = np.sign(normalized_spread).diff() / 2
    sell[0] = 0

    orders = below_neg_1.astype(int) - above_1.astype(int) - sell.astype(int)
    return orders.map(
        lambda x: pm.Buy("eth", 1, fraction=True)
        if x == 1
        else pm.Sell("eth", 1, fraction=True)
        if x == -1
        else pm.Nop()
    )


pm.add_strategy(btc_strat)
pm.add_strategy(eth_strat)
pm.run()
print(pm.portfolio_value())

print(pm.investments)
