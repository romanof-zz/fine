import csv
import yaml
from .analyzers import Ticker

class TickerConfig:
    def __init__(self, root):
        self.root = root
        with open("{dir}/config/ticker.yaml".format(dir=root), 'r') as data:
            self.config = yaml.load(data, Loader=yaml.BaseLoader)

    def parser(self):
        return TickerParser(self.root)

    def default_stocks(self):
        return self.config["stocks"]

class TickerParser:
    def __init__(self, root):
        self.root = "{dir}/datasets/tickers".format(dir=root)

    def parse_daily(self, stocks):
        tickers = []
        for stock in stocks:
            file = "{dir}/{stock}_{type}.csv".format(dir=self.root, stock=stock, type=Ticker.DAILY)
            with open(file, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                next(reader, None)  # skip the headers
                for row in reader:
                    tickers.append(Ticker.init_daily(stock, row))
        return tickers
