from datetime import date
from datetime import datetime
import time
import csv
import io
import yaml
import urllib.request
from urllib.error import HTTPError
from botocore.exceptions import ClientError
from .models import Ticker, Stock
from .symbols import US_SYMBOLS

class StockDataAccess:
    DAILY_FILE = "stocks/us.stocks.daily"
    INTRADAY_FILE = "stocks/us.stocks.intraday"

    def __init__(self, logger, storage):
        self.logger = logger
        self.storage = storage

    def load_all(self):
        return map(lambda s: Stock(s, None, None, None, None), US_SYMBOLS)

    def load_one(self, symbol):
        return Stock(symbol, None, None, None, None)

    def load_not_updated(self, type, limit):
        file = self.DAILY_FILE if type == Ticker.DAILY else self.INTRADAY_FILE
        sdata = self.storage.get(file)
        if not sdata:
            sdata = ",".join(US_SYMBOLS)
            self.storage.put(file, sdata)

        stocks = sdata.split(",")
        if type == Ticker.DAILY:
            self.daily = stocks
        else:
            self.intraday = stocks

        self.logger.info("type {t} total: {cnt}".format(t=type, cnt=len(stocks)))
        return stocks[:limit]

    def update_now(self, symbol, type):
        stocks = self.daily if type == Ticker.DAILY else self.intraday
        stocks.remove(symbol)
        sdata = ",".join(stocks) if stocks else ''
        file = self.DAILY_FILE if type == Ticker.DAILY else self.INTRADAY_FILE
        self.storage.put(file, sdata)

class TickerDataAccess:
    DIR = "tickers"

    DAILY_URL_BASE = "https://query1.finance.yahoo.com/v7/finance/download"
    DAILY_EVENTS = "history"
    DAILY_INTERVAL = "1d"

    INTRADAY_URL_BASE = "https://www.alphavantage.co/query"
    INTRADAY_FUNC = "TIME_SERIES_INTRADAY"
    INTRADAY_TIMEOUT = 15

    def __init__(self, stock_access, storage, logger, token, auth_cookie, app_key):
        self.stock_access = stock_access
        self.storage = storage
        self.logger = logger
        self.token = token
        self.auth_cookie = auth_cookie
        self.app_key = app_key

    def update_daily(self, symbols):
        cookieProcessor = urllib.request.HTTPCookieProcessor()
        opener = urllib.request.build_opener(cookieProcessor)
        opener.addheaders.append(('Cookie', "B={c}".format(c=self.auth_cookie)))

        for symbol in symbols:
            url = "{b}/{s}?period1={p1}&period2={p2}&interval={i}&events={e}&crumb={t}".format(
                b=self.DAILY_URL_BASE, s=symbol, p1=0, p2=int(time.time()),
                i=self.DAILY_INTERVAL, e=self.DAILY_EVENTS, t=self.token)
            try:
                self.logger.info("daily update {}".format(symbol))
                self.logger.debug("update url: {}".format(url))
                self.storage.put(self.__name_key(symbol, Ticker.DAILY), opener.open(url).read())
                self.logger.info("finished updating {}".format(symbol))
            except HTTPError:
                self.logger.error("{} failed to update".format(symbol))
            finally:
                self.stock_access.update_now(symbol, Ticker.DAILY)

    def update_intraday(self, symbols):
        error = False
        for symbol in symbols:
            try:
                self.logger.info("{s} loading data".format(s=symbol))

                url = "{}?function={}&symbol={}&interval={}&apikey={}&outputsize=compact&datatype=csv".format(
                    self.INTRADAY_URL_BASE, self.INTRADAY_FUNC, symbol, Ticker.INTRADAY, self.app_key)
                self.logger.debug("stock url: {}".format(url))
                data = urllib.request.urlopen(url).read().decode("utf-8")
                reader = csv.reader(io.StringIO(data), delimiter=',')
                header = next(reader, None)  # skip the headers

                tickers = {}
                for row in reader:
                    try:
                        self.logger.debug("getting data for {}".format(row[0]))
                        t = datetime.strptime(row[0], Ticker.INTRADAY_TIME_FORMAT)
                        date_key = t.strftime(Ticker.DAILY_TIME_FORMAT)
                        if not date_key in tickers: tickers[date_key] = []
                        tickers[date_key].append(Ticker(Ticker.INTRADAY, symbol, t, row[1], row[4], row[3], row[2], "0.0", row[5]))
                    except ValueError as e:
                        self.logger.error("failed to load intraday row for {s} stock with error: {e}".format(s=symbol, e=str(e)))
                        error = True
                        break

                if error:
                    self.logger.info("sleep for {} sec".format(self.INTRADAY_TIMEOUT))
                    time.sleep(self.INTRADAY_TIMEOUT)
                    error = False
                    continue

                for key in tickers:
                    data = "time,open,close,low,high,adj_close,volume\n"
                    data += "\n".join(map(lambda t: t.to_csv(), tickers[key]))
                    self.storage.put(self.__name_key(symbol, key), data)
                    self.logger.info("finished updating {k}".format(k=key))

                if tickers:
                    self.logger.info("{s} marked updated".format(s=symbol))

            except HTTPError as ex:
                self.logger.error("{s} failed intraday update with error {e}".format(s=symbol, e=str(ex)))
            finally:
                self.stock_access.update_now(symbol, Ticker.INTRADAY)

    def load_daily(self, stock):
        return self.__load(stock, Ticker.DAILY, Ticker.DAILY, Ticker.DAILY_TIME_FORMAT)

    def load_intraday(self, stock, date):
        tickers = self.__load(stock, Ticker.INTRADAY, date.strftime(Ticker.DAILY_TIME_FORMAT), Ticker.INTRADAY_TIME_FORMAT)
        # intraday tickers are recorded in reverse order
        return list(reversed(tickers))

    def __load(self, stock, type, key, time_format):
        tickers = []
        filename = self.__name_key(stock.symbol, key)
        reader = csv.reader(io.StringIO(self.storage.get(filename)), delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            try:
                time = datetime.strptime(row[0], time_format)
                tickers.append(Ticker(type, stock, time, row[1], row[2], row[3], row[4], row[5], row[6]))
            except ValueError:
                continue
        return tickers

    def __name_key(self, symbol, key):
        return "{dir}/{s}/{k}.csv".format(dir=self.DIR, s=symbol, k=key)
