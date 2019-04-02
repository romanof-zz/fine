import csv
from .models import Ticker

class TickerParser:
    def __init__(self, root):
        self.root = "{dir}/datasets/tickers/".format(dir=root)

    def parse_daily(self, stock):
        tickers = []
        with open("{dir}/{stock}_{type}.csv".format(dir=self.root, stock=stock, type=Ticker.DAILY), 'r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader, None)  # skip the headers
            for row in reader:
                tickers.append(Ticker.init_daily(stock, row))
        return tickers
