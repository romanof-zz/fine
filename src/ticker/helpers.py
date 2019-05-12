import time
import csv
import urllib.request

from .analyzers import Ticker

def daily_name(stock):
    return "{}_{}.csv".format(stock, Ticker.DAILY)

class TickerUpdater:
    URL_BASE = "https://query1.finance.yahoo.com/v7/finance/download"
    EVENTS = "history"
    INTERVAL = "1d"

    def __init__(self, storage, stocks, token, auth_cookie):
        self.storage = storage
        self.stocks = stocks
        self.token = token
        self.auth_cookie = auth_cookie

    def update_daily(self):
        cookieProcessor = urllib.request.HTTPCookieProcessor()
        opener = urllib.request.build_opener(cookieProcessor)
        opener.addheaders.append(('Cookie', "B={c}".format(c=self.auth_cookie)))

        for stock in self.stocks:
            url = "{b}/{s}?period1={p1}&period2={p2}&interval={i}&events={e}&crumb={t}".format(
                b=self.URL_BASE, s=stock, p1=0, p2=int(time.time()),
                i=self.INTERVAL, e=self.EVENTS, t=self.token)
            print("=== loading {s} via {url} ===".format(s=stock, url=url))

            data = opener.open(url).read()
            self.storage.put(daily_name(stock), data)

            print("=== finished updating {s} ===".format(s=stock))

class TickerParser:
    def __init__(self, storage):
        self.storage = storage

    def parse_daily(self, stocks):
        tickers = []
        for stock in stocks:
            reader = csv.reader(self.storage.get(daily_name(stock)), delimiter=',')
            next(reader, None)  # skip the headers
            for row in reader:
                try:
                    tickers.append(Ticker.init_daily(stock, row))
                except (ValueError):
                    continue
        return tickers
