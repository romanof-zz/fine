import logging
import os
from datetime import timedelta

from storage import LocalCachedS3Storage

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

        self.s3 = LocalCachedS3Storage(self.APP_BUCKET, os.environ.get('FINE_CACHE_ENABLED', False))
        self.stock_access = StockDataAccess()
        self.ticker_access = TickerDataAccess(self.s3, self.logger)
        self.twitter_access = TwitterDataAccess(self.s3, self.logger,
                                                os.environ.get('FINE_TWEETER_CONSUMER_KEY', ''),
                                                os.environ.get('FINE_TWEETER_CONSUMER_SECRET', ''),
                                                os.environ.get('FINE_TWEETER_ACCESS_TOKEN', ''),
                                                os.environ.get('FINE_TWEETER_ACCESS_SECRET', ''))

        self.simulator = Simulator(self.logger, self.ticker_access)

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

    def load_tickers(self, stock):
        return self.ticker_access.load(stock.symbol, Ticker.Type.ONE_DAY)

    def update(self, symbols, type, period, limit):
        if not symbols: symbols = self.ticker_access.symbols2update(type, limit)
        if symbols: self.ticker_access.update(symbols, type, period)

    def twitter_update(self):
        self.twitter_access.update_all()

def lambda_ticker_update(event, context):
    app = AppContext()
    app.logger.info("started 1d ticker update")
    app.update(None, Ticker.Type.ONE_DAY, 'max', 100)
    app.logger.info("started 1h ticker update")
    app.update(None, Ticker.Type.ONE_HOUR, 1, 100)
    app.logger.info("started 5m ticker update")
    app.update(None, Ticker.Type.FIVE_MIN, 1, 100)
    app.logger.info("started 1m ticker update")
    app.update(None, Ticker.Type.ONE_MIN, 1, 100)
    app.logger.info("started options update")
    app.update(None, Ticker.Type.OPTIONS, 1, 100)
    app.logger.info("finished all ticker updates")
    return {'resultCode': 200}

def lambda_twitter_update(event, context):
    app = AppContext()
    app.logger.info("started twitter update")
    app.twitter_update()
    app.logger.info("finished twitter update")
    return {'resultCode': 200}
