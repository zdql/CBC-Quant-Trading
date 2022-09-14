from . import Test


class Spot:
    def __init__(self, line, currency):
        self.currency = currency
        self.price = calculate_value(line)

    def calculate_value(line):
        df = line[["startTime", "close"]]
        df.columns = ["time", "price"]
        df = df.set_index("time")
        return df
