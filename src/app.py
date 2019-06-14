import logging
import os
from storage import S3Storage
from stocks.data_access import StockDataAccess, TickerDataAccess
from stocks.models import Ticker

class AppContext:
    APP_BUCKET = "fine.data"
    DB_NAME = 'fine'

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        self.s3 = S3Storage(self.APP_BUCKET)
        self.stock_access = StockDataAccess(self.s3)
        self.ticker_access = TickerDataAccess(self.root, self.stock_access, self.s3, self.logger,
                                              os.environ["FINE_YAHOO_TOKEN"],
                                              os.environ["FINE_YAHOO_COOKIE"],
                                              os.environ["FINE_ALPHAVANTAGE_KEY"])

    def update(self, stock, type, limit):
        stocks = [self.stock_access.load_one(stock)] if stock is not None else self.stock_access.load_not_updated(type, limit)
        self.ticker_access.update_intraday(stocks)

APP = AppContext()

def lambda_update_daily(context, data):
    APP.update(None, Ticker.DAILY, 30)

def lambda_update_intraday(context, data):
    APP.update(None, Ticker.INTRADAY, 30)
