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

class StockDataAccess:
    FILE = "stocks/all.yml"

    def __init__(self, logger, storage):
        self.logger = logger
        self.storage = storage
        stocks = yaml.load(self.storage.get(self.FILE), Loader=yaml.FullLoader)
        self.stocks = [] if stocks is None else stocks

    def load_updated_today(self):
        return filter(lambda s: s.daily_updated > datetime.combine(date.today(), datetime.min.time()), self.stocks)

    def load_one(self, symbol):
        return next(filter(lambda s: s.symbol == symbol, self.stocks) or [], None)

    def load_not_updated(self, type, limit):
        update_prop = "daily_updated" if type == Ticker.DAILY else "intraday_updated"
        today_start = datetime.combine(date.today(), datetime.min.time())
        stocks = list(filter(lambda s: getattr(s, update_prop) < today_start, self.stocks))
        self.logger.info("type {t} total: {cnt}".format(t=type, cnt=len(stocks)))
        return stocks[:limit]

    def update_now(self, stock, type):
        loaded_stock = self.load_one(stock.symbol)
        if type == Ticker.DAILY:
            loaded_stock.daily_updated = datetime.utcnow()
        if type == Ticker.INTRADAY:
            loaded_stock.intraday_updated = datetime.utcnow()

    def store(self):
        self.storage.put(self.FILE, yaml.dump(self.stocks))

class TickerDataAccess:
    DIR = "tickers"

    DAILY_URL_BASE = "https://query1.finance.yahoo.com/v7/finance/download"
    DAILY_EVENTS = "history"
    DAILY_INTERVAL = "1d"

    INTRADAY_URL_BASE = "https://www.alphavantage.co/query"
    INTRADAY_FUNC = "TIME_SERIES_INTRADAY"
    INTRADAY_TIMEOUT = 15

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
                self.logger.info("daily update {}".format(stock.symbol))
                self.logger.debug("update url: {}".format(url))
                self.storage.put(self.__name_key(stock.symbol, Ticker.DAILY), opener.open(url).read())
                self.stock_access.update_now(stock, Ticker.DAILY)
                self.logger.info("finished updating {}".format(stock.symbol))
            except HTTPError:
                self.logger.error("{} failed to update".format(stock.symbol))
        self.stock_access.store()

    def update_intraday(self, stocks):
        error = False
        for stock in stocks:
            try:
                self.logger.info("{s} loading data".format(s=stock.symbol))

                url = "{}?function={}&symbol={}&interval={}&apikey={}&outputsize=compact&datatype=csv".format(
                    self.INTRADAY_URL_BASE, self.INTRADAY_FUNC, stock.symbol, Ticker.INTRADAY, self.app_key)
                self.logger.debug("stock url: {}".format(url))
                data = urllib.request.urlopen(url).read().decode("utf-8")
                reader = csv.reader(io.StringIO(data), delimiter=',')
                header = next(reader, None)  # skip the headers

                tickers = {}
                for row in reader:
                    try:
                        self.logger.debug("getting data for {}".format(row[0]))
                        t = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                        date_key = t.strftime('%Y-%m-%d')
                        if not date_key in tickers: tickers[date_key] = []
                        tickers[date_key].append(Ticker(Ticker.INTRADAY, stock.symbol, t, row[1], row[4], row[3], row[2], "0.0", row[5]))
                    except ValueError as e:
                        self.logger.error("failed to load intraday row for {s} stock with error: {e}".format(s=stock.symbol, e=str(e)))
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
                    self.storage.put(self.__name_key(stock.symbol, key), data)
                    self.logger.info("finished updating {k}".format(k=key))

                if tickers:
                    self.stock_access.update_now(stock, Ticker.INTRADAY)
                    self.logger.info("{s} marked updated".format(s=stock.symbol))

            except HTTPError as ex:
                self.logger.error("{s} failed intraday update with error {e}".format(s=stock.symbol, e=str(ex)))

        self.stock_access.store()

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
                        time = datetime.strptime(row[0], '%Y-%m-%d')
                        tickers.append(Ticker(type, stock.symbol, time, row[1], row[2], row[3], row[4], row[5], row[6]))
                    except ValueError:
                        continue
            except ClientError:
                self.logger.error("{k} file failed to load.".format(k=key))
        return tickers

    def __name_key(self, symbol, key):
        return "{dir}/{s}/{k}.csv".format(dir=self.DIR, s=symbol, k=key)
