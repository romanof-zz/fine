class Ticker:
    DAILY = "daily"

    def __init__(self, type, stock, date, open, close, low, high, adj_close, volume):
        self.type = type
        self.stock = stock
        self.date = date
        self.open = open
        self.close = close
        self.low = low
        self.high = high
        self.adj_close = adj_close
        self.volume = volume

    @classmethod
    def init_daily(self, stock, row):
        return self(self.DAILY, stock, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
