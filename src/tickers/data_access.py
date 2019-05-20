import time
import csv
import urllib.request

from .models import Ticker

class TickerDataAccess:
    URL_BASE = "https://query1.finance.yahoo.com/v7/finance/download"
    EVENTS = "history"
    INTERVAL = "1d"

    def __init__(self, root, token, auth_cookie):
        self.path = "{dir}/.cache/tickers".format(dir=root)
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
            data = opener.open(url).read()
            with open(self.__name_path(stock, Ticker.DAILY), 'wb') as file:
                file.write(data)
            print("=== finished updating {s} ===".format(s=stock))

    def load(self, stocks):
        return self.__load(stocks, Ticker.DAILY)

    def __load(self, stocks, type):
        tickers = []
        for stock in stocks:
            with open(self.__name_path(stock, Ticker.DAILY), 'r') as file:
                reader = csv.reader(file, delimiter=',')
                next(reader, None)  # skip the headers
                for row in reader:
                    try:
                        tickers.append(Ticker(type, stock, row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    except (ValueError):
                        continue
        return tickers

    def __name_path(self, stock, type):
        return "{}/{}_{}.csv".format(self.path, stock, type)
