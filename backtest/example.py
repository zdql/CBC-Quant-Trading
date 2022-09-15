from pm import PortfolioManager
import pandas as pd
import numpy as np
from functools import partial
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

pm = PortfolioManager(1000)

btc_close = pd.read_csv("../data/BTC/USD.csv", index_col="time").close
pm.link_data("btc", btc_close)


def my_strat(data, buy_frac=0.1, sell_frac=0.1):

    diff = data["btc"].diff()

    increasing_run = diff.groupby(diff.lt(0).cumsum()).cumcount()
    decreasing_run = diff.groupby(diff.gt(0).cumsum()).cumcount()
    runs = increasing_run - decreasing_run

    orders = runs.map(
        lambda x: pm.Buy("btc", buy_frac, fraction=True)
        if x == 4
        else pm.Sell("btc", sell_frac, fraction=True)
        if x == -4
        else pm.Nop()
    )

    return orders


fractions = np.linspace(0.1, 1, 10)
frac_pairs = np.array(np.meshgrid(fractions, fractions)).T
results = np.zeros(frac_pairs.shape[:-1])

it = np.nditer(frac_pairs, flags=["multi_index"], op_axes=[[0, 1]])
for _ in it:
    idx = it.multi_index
    fracs = frac_pairs[idx]
    kwargs = {"buy_frac": fracs[0], "sell_frac": fracs[1]}
    strat = partial(my_strat, **kwargs)
    pm.add_strategy(strat)
    pm.run()
    results[idx] = pm.portfolio_value()
    pm.reset()

cmap = LinearSegmentedColormap.from_list(name="rwg", colors=["red", "white", "green"])
results = results[::-1]
fmt_fractions = pd.Series(fractions).map(lambda frac: f"{frac:.0%}")
ax = sns.heatmap(
    results,
    cmap=cmap,
    square=True,
    xticklabels=fmt_fractions,
    yticklabels=fmt_fractions[::-1],
)
ax.set(
    title="Profit from Momentum Strategies",
    xlabel="Sell Fraction",
    ylabel="Buy Fraction",
)
plt.show()
