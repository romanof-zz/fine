import datetime

class Ticker:
    DAILY = "daily"

    def __init__(self, type, stock, date, open, close, low, high, adj_close, volume):
        self.type = type
        self.stock = stock
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.open = float(open)
        self.close = float(close)
        self.low = float(low)
        self.high = float(high)
        self.adj_close = float(adj_close)
        self.volume = int(volume)

    @classmethod
    def init_daily(self, stock, row):
        return self(self.DAILY, stock, row[0], row[1], row[2], row[3], row[4], row[5], row[6])
