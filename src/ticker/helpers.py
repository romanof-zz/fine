import time
import csv
import yaml
import urllib.request

from .analyzers import Ticker

class TickerConfig:
    def __init__(self, root):
        self.root = root
        with open("{dir}/config/ticker.yaml".format(dir=root), 'r') as data:
            self.config = yaml.load(data, Loader=yaml.BaseLoader)

    def parser(self):
        return TickerParser(self.root)

    def updater(self, stocks):
        return TickerUpdater(
            self.root,
            stocks,
            self.config['updater']['token'],
            self.config['updater']['auth_cookie'])

    def default_stocks(self):
        return self.config["stocks"]

class TickerUpdater:
    URL_BASE = "https://query1.finance.yahoo.com/v7/finance/download"
    EVENTS = "history"
    INTERVAL = "1d"

    def __init__(self, root, stocks, token, auth_cookie):
        self.root = "{dir}/datasets/tickers".format(dir=root)
        self.stocks = stocks
        self.token = token
        self.auth_cookie = auth_cookie

    def update_daily(self):
        cookieProcessor = urllib.request.HTTPCookieProcessor()
        opener = urllib.request.build_opener(cookieProcessor)
        opener.addheaders.append(('Cookie', "B={c}".format(c=self.auth_cookie)))

        for stock in self.stocks:
            url = "{b}/{s}?period1={p1}&period2={p2}&interval={i}&events={e}&crumb={t}".format(
                b=self.URL_BASE,
                s=stock,
                p1=0,
                p2=int(time.time()),
                i=self.INTERVAL,
                e=self.EVENTS,
                t=self.token)
            print("=== loading {s} via {url} ===".format(s=stock, url=url))
            # Cookie: B=60s3hqte9dlv9&b=3&s=it; GUC=AQEBAQFcm-1dekIdygR3&s=AQAAAHJqYVlu&g=XJqo6A; PRF=t%3DGOOG%252BMSFT%252BAMZN
            data = opener.open(url).read()
            with open("{r}/{s}_{t}.csv".format(r=self.root, s=stock, t=Ticker.DAILY), 'wb') as file:
                file.write(data)
            print("=== finished updating {s} ===".format(s=stock))

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
                    try:
                        tickers.append(Ticker.init_daily(stock, row))
                    except (ValueError):
                        continue
        return tickers
