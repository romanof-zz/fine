import logging
import os
from storage import S3Storage
from stocks.data_access import StockDataAccess, TickerDataAccess
from stocks.models import Ticker

class AppContext:
    APP_BUCKET = "fine.data"
    DB_NAME = 'fine'

    def __init__(self):
        self.logger = logging.getLogger()
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
        logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',level=logging.INFO)

        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        self.s3 = S3Storage(self.APP_BUCKET)
        self.stock_access = StockDataAccess(self.logger, self.s3)
        self.ticker_access = TickerDataAccess(self.root, self.stock_access, self.s3, self.logger,
                                              os.environ["FINE_YAHOO_TOKEN"],
                                              os.environ["FINE_YAHOO_COOKIE"],
                                              os.environ["FINE_ALPHAVANTAGE_KEY"])

    def update(self, stock, type, limit):
        try:
            self.logger.info("update {t} type: requested {l} items".format(t=type, l=limit))
            stocks = [self.stock_access.load_one(stock)] if stock is not None else self.stock_access.load_not_updated(type, limit)
            if type == Ticker.INTRADAY:
                self.ticker_access.update_intraday(stocks)
            if type == Ticker.DAILY:
                self.ticker_access.update_daily(stocks)
        except KeyboardInterrupt:
            self.logger.error("properly finalizing interput")
            self.stock_access.store()

def lambda_update(event, context):
    app = AppContext()

    for x in range(0,5):
        app.logger.info("update iter #{}".format(x))
        app.update(None, Ticker.DAILY, 5)
        app.update(None, Ticker.INTRADAY, 5)

    app.logger.info("all updates finished.")
    return {'resultCode': 200}
