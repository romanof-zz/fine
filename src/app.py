import logging
import os

from storage import S3Storage

from stocks.access import StockDataAccess, TickerDataAccess
from stocks.analyzers import TickerAnalyzer
from stocks.models import Ticker, TickerAnalysisStats, TickerAnalysisResult

from bets.models import Signal
from bets.simulator import Simulator

from sentiment.access import TwitterDataAccess

class AppContext:
    APP_BUCKET = "fine.data"

    def __init__(self):
        self.logger = logging.getLogger()
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
        logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',level=logging.INFO)

        self.s3 = S3Storage(self.APP_BUCKET)
        self.stock_access = StockDataAccess(self.logger, self.s3)
        self.ticker_access = TickerDataAccess(self.stock_access, self.s3, self.logger,
                                              os.environ["FINE_YAHOO_TOKEN"],
                                              os.environ["FINE_YAHOO_COOKIE"],
                                              os.environ["FINE_ALPHAVANTAGE_KEY"])
        self.twitter_access = TwitterDataAccess(self.s3, self.logger,
                                                os.environ['FINE_TWEETER_CONSUMER_KEY'],
                                                os.environ['FINE_TWEETER_CONSUMER_SECRET'],
                                                os.environ['FINE_TWEETER_ACCESS_TOKEN'],
                                                os.environ['FINE_TWEETER_ACCESS_SECRET'])

        self.simulator = Simulator(self.logger, self.ticker_access)

    def load_tickers(self, stock):
        return self.ticker_access.load_daily(stock)

    def load_stocks(self, stock, updated_only):
        if stock is not None:
            return [self.stock_access.load_one(stock)]
        elif updated_only:
            return self.stock_access.load_updated_today()
        else:
            return self.stock_access.stocks

    def analyze(self, tickers, period, function, threshold):
        results = TickerAnalyzer(tickers, self.logger).analyze(period, function)
        # flatten stats
        stats = [result.stats[frame][type] for type in TickerAnalysisStats.TYPES for frame in TickerAnalysisResult.RESULT_FRAMES for result in results]
        # filter above threshold
        stats = filter(lambda s: s.chance >= threshold and s.percent_change > 0 , stats)
        # sort by chance, sample size and highest gain accordingly.
        stats = sorted(stats, key = lambda s: (s.chance, s.count, s.percent_change), reverse=True)

        return Signal.from_ticker_stat(stats[0]) if len(stats) else None

    def simulate(self, signal):
        return self.simulator.simulate(signal)

    def update(self, stock, type, limit):
        try:
            self.logger.info("update {t} type: requested {l} items".format(t=type, l=limit))
            stocks = [self.stock_access.load_one(stock)] if stock is not None else self.stock_access.load_not_updated(type, limit)
            if not len(stocks): return False
            if type == Ticker.INTRADAY:
                self.ticker_access.update_intraday(stocks)
            if type == Ticker.DAILY:
                self.ticker_access.update_daily(stocks)
            return True
        except KeyboardInterrupt:
            self.logger.error("properly finalizing interput")
            self.stock_access.store()

    def twitter_update(self):
        self.twitter_access.update_all()

def lambda_ticker_update(event, context):
    app = AppContext()

    for x in range(0,5):
        app.logger.info("update iter #{}".format(x))
        daily_result = app.update(None, Ticker.DAILY, 5)
        intraday_result = app.update(None, Ticker.INTRADAY, 5)
        if not daily_result and not intraday_result: break

    app.logger.info("all updates finished.")
    return {'resultCode': 200}

def lambda_twitter_update(event, context):
    app = AppContext()
    app.twitter_update()
    app.logger.info("all updates finished.")
    return {'resultCode': 200}
