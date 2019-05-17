import time
import csv
import urllib.request

from .models import Ticker

class TickerDataAccess:
    URL_BASE = "https://query1.finance.yahoo.com/v7/finance/download"
    EVENTS = "history"
    INTERVAL = "1d"

    def __init__(self, storage, token, auth_cookie):
        self.storage = storage.with_bucket('fine.tickers')
        self.token = token
        self.auth_cookie = auth_cookie

    def update(self, stocks):
        cookieProcessor = urllib.request.HTTPCookieProcessor()
        opener = urllib.request.build_opener(cookieProcessor)
        opener.addheaders.append(('Cookie', "B={c}".format(c=self.auth_cookie)))

        for stock in stocks:
            url = "{b}/{s}?period1={p1}&period2={p2}&interval={i}&events={e}&crumb={t}".format(
                b=self.URL_BASE, s=stock, p1=0, p2=int(time.time()),
                i=self.INTERVAL, e=self.EVENTS, t=self.token)
            print("=== loading {s} via {url} ===".format(s=stock, url=url))

            data = opener.open(url).read()
            self.storage.put(self.__name(stock, Ticker.DAILY), data)

            print("=== finished updating {s} ===".format(s=stock))

    def load(self, stocks):
        return self.__load(stocks, Ticker.DAILY)

    def __load(self, stocks, type):
        tickers = []
        for stock in stocks:
            reader = csv.reader(self.storage.get(self.__name(stock, type)), delimiter=',')
            next(reader, None)  # skip the headers
            for row in reader:
                try:
                    tickers.append(Ticker(type, stock, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                except (ValueError):
                    continue
        return tickers

    def __name(self, stock, type):
        return "{}_{}.csv".format(stock, type)
