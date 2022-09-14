from lines.line import Line
from utils import get_instances
from vocabulary import Vocabulary


class PortfolioManager:
    def __init__(self, starting_cash):
        self.data = {}
        self.time = None
        self.money = starting_cash
        self.transactions = get_instances("transactions")
        self.strategies = []

    def link_data(self, name, data):
        self.data[name] = Line(data)
        self.time = min(self.time, self.data[name].t0)

    # def add_strategy(self, strategy):
    #     self.strategies.append(Vocabulary.parse_cmd(strategy))

    def add_strategy(self, strategy, *args, **kwargs):
        self.strategies.append(strategy, *args, **kwargs)

    def run(self):
        pass


if __name__ == "__main__":
    pm = PortfolioManager(1000)

    def my_strat(d1):
        moved_up = d1.Close - d1.Close.shift()
        orders = None
