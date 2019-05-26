import datetime
import time
import csv
import io
import urllib.request
from urllib.error import HTTPError
from botocore.exceptions import ClientError
from .models import Ticker, Stock

class StockDataAccess:
    def __init__(self, storage):
        self.storage = storage

    def all_updated_today(self):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        return self.__load("select * from fine.stocks where daily_updated = timestamp('{}') and deleted = 0".format(date))

    def load_one(self, symbol):
        return self.__load("select * from fine.stocks where symbol='{}'".format(symbol))[0]

    def load_not_updated(self, type, limit=None):
        field = "daily_updated" if type != Ticker.INTRADAY else "intraday_updated"
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        q = "select * from fine.stocks where {} < timestamp('{}') and deleted = 0".format(field, date)
        if limit: q += " limit {}".format(limit)
        return self.__load(q)

    def update_date(self, type, stock):
        field = "daily_updated" if type != Ticker.INTRADAY else "intraday_updated"
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.storage.execute("update fine.stocks set {} = timestamp('{}') where symbol='{}'".format(field, date, stock.symbol))

    def __load(self, query):
        return [Stock(row[0],row[1], row[2], row[3], row[4], row[6], row[5],
                      row[7], row[8]) for row in self.storage.load(query)]

class TickerDataAccess:
    DIR = "tickers"

    DAILY_URL_BASE = "https://query1.finance.yahoo.com/v7/finance/download"
    DAILY_EVENTS = "history"
    DAILY_INTERVAL = "1d"

    INTRADAY_URL_BASE = "https://www.alphavantage.co/query"
    INTRADAY_FUNC = "TIME_SERIES_INTRADAY"

    def __init__(self, root, stock_access, storage, logger, token, auth_cookie, app_key):
        self.path = "{r}/.cache".format(r=root)
        self.stock_access = stock_access
        self.storage = storage
        self.logger = logger
        self.token = token
        self.auth_cookie = auth_cookie
        self.app_key = app_key

    def update_daily(self, stocks):
        cookieProcessor = urllib.request.HTTPCookieProcessor()
        opener = urllib.request.build_opener(cookieProcessor)
        opener.addheaders.append(('Cookie', "B={c}".format(c=self.auth_cookie)))

        for stock in stocks:
            url = "{b}/{s}?period1={p1}&period2={p2}&interval={i}&events={e}&crumb={t}".format(
                b=self.DAILY_URL_BASE, s=stock.symbol, p1=0, p2=int(time.time()),
                i=self.DAILY_INTERVAL, e=self.DAILY_EVENTS, t=self.token)
            try:
                self.storage.put(self.__name_key(stock.symbol, Ticker.DAILY), opener.open(url).read())
                self.stock_access.update_date(Ticker.DAILY, stock)
                self.logger.info("=== finished updating {s} ===".format(s=stock.symbol))
            except HTTPError:
                self.logger.error("=== {s} failed to update ===".format(s=stock.symbol))

    def update_intraday(self, stocks):
        for stock in stocks:
            try:
                url = "{}?function={}&symbol={}&interval={}&apikey={}&outputsize=full&datatype=csv".format(
                    self.INTRADAY_URL_BASE, self.INTRADAY_FUNC, stock.symbol, Ticker.INTRADAY, self.app_key)
                data = urllib.request.urlopen(url).read().decode("utf-8")
                self.logger.info("=== loaded intraday values of {s} ===".format(s=stock.symbol))
                reader = csv.reader(io.StringIO(data), delimiter=',')
                next(reader, None)  # skip the headers
                tickers = {}
                for row in reader:
                    try:
                        t = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                        date_key = t.strftime('%Y-%m-%d')
                        if not date_key in tickers: tickers[date_key] = []
                        tickers[date_key].append(Ticker(Ticker.INTRADAY, stock.symbol, t, row[1], row[4], row[3], row[2], "0.0", row[5]))
                    except ValueError:
                        continue

                for key in tickers:
                    data = "time,open,close,low,high,adj_close,volume\n"
                    data += "\n".join(map(lambda t: t.to_csv(), tickers[key]))
                    self.storage.put(self.__name_key(stock.symbol, key), data)
                    self.logger.info("=== finished updating {k} ===".format(k=key))

                self.stock_access.update_date(Ticker.INTRADAY, stock)
                time.sleep(5)
            except HTTPError as ex:
                self.logger.error("=== {s} failed intraday update with error {e} ===".format(s=stock.symbol, e=str(ex)))

    def load(self, stocks):
        return self.__load(stocks, Ticker.DAILY)

    def __load(self, stocks, type):
        tickers = []
        for stock in stocks:
            key = self.__name_key(stock.symbol, type)
            try:
                reader = csv.reader(io.StringIO(self.storage.get(key)), delimiter=',')
                next(reader, None)  # skip the headers
                for row in reader:
                    try:
                        time = datetime.datetime.strptime(row[0], '%Y-%m-%d')
                        tickers.append(Ticker(type, stock.symbol, time, row[1], row[2], row[3], row[4], row[5], row[6]))
                    except ValueError:
                        continue
            except ClientError:
                self.logger.error("{k} file failed to load.".format(k=key))
        return tickers

    def __name_key(self, symbol, key):
        return "{dir}/{s}/{k}.csv".format(dir=self.DIR, s=symbol, k=key)
