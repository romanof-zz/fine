import logging
import os
from datetime import timedelta

from storage import S3Storage

from stocks.access import StockDataAccess, TickerDataAccess
from stocks.analyzers import TickerAnalyzer
from stocks.models import Ticker, TickerAnalysisStats

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
        return self.ticker_access.load_daily(stock.symbol)

    def load_stocks(self, symbol):
        return self.stock_access.load_all() if symbol is None else self.stock_access.load_one(symbol)

    def analyze_timeframe(self, stock, period, function, threshold, date, interval, frame, invert):
        signals = []
        tickers = self.load_tickers(stock)
        for d in range(0, interval):
            signal = self.analyze(list(filter(lambda t: t.time <= date - timedelta(days=d), tickers)),
                period, function, threshold, frame, invert)
            if signal: signals.append(signal)

        self.logger.info("loaded {} tickers & produced {} signals for {}".format(len(tickers), len(signals), stock.symbol))
        return signals

    def analyze(self, tickers, period, function, threshold, frame, invert):
        results = TickerAnalyzer(tickers, self.logger, frame).analyze(period, function)
        # flatten stats
        stats = []
        for result in results:
            for frame in result.frames:
                stats += [result.stats[frame][type] for type in TickerAnalysisStats.TYPES]

        # filter above threshold
        stats = filter(lambda s: s.chance >= threshold and s.percent_change > 0 , stats)
        # sort by chance, sample size and highest gain accordingly.
        stats = sorted(stats, key = lambda s: (s.chance, s.count, s.percent_change), reverse=True)

        return Signal.from_ticker_stat(stats[0], invert) if len(stats) else None

    def simulate(self, signal):
        return self.simulator.simulate(signal)

    def update(self, symbol, type, limit):
        self.logger.info("update {t} type: requested {l} items".format(t=type, l=limit))
        symbols = self.stock_access.load_not_updated(type, limit) if symbol is None else [symbol]
        if not len(symbols): return False
        if type == Ticker.INTRADAY:
            self.ticker_access.update_intraday(symbols)
        if type == Ticker.DAILY:
            self.ticker_access.update_daily(symbols)
        return True

    def twitter_update(self):
        self.twitter_access.update_all()

def lambda_ticker_daily_update(event, context):
    app = AppContext()
    app.logger.info("started daily update")
    app.update(None, Ticker.DAILY, 300)
    app.logger.info("finished daily update")
    return {'resultCode': 200}

def lambda_ticker_intraday_update(event, context):
    app = AppContext()
    app.logger.info("started intraday update")
    app.update(None, Ticker.INTRADAY, 5)
    app.logger.info("finished daily update")
    return {'resultCode': 200}

def lambda_twitter_update(event, context):
    app = AppContext()
    app.logger.info("started twitter update")
    app.twitter_update()
    app.logger.info("finished twitter update")
    return {'resultCode': 200}
