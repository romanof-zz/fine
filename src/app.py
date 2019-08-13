import logging
import os
import boto3

from datetime import timedelta


from storage import LocalCachedS3Storage

from stocks.access import StockDataAccess, TickerDataAccess
from stocks.analyzers import TickerAnalyzer
from stocks.models import Ticker, TickerAnalysisStats

from bets.models import Signal
from bets.simulator import Simulator

from sentiment.access import TwitterDataAccess
from sentiment.analyzers import SentimentAnalyzer

class AppContext:
    APP_BUCKET = "fine.data"
    APP_BUILDS = "fine.builds"
    APP_PKG_NAME = "lambda.zip"

    def __init__(self):
        self.__taccess = None
        self.__saccess = None
        self.__twaccess = None

        self.logger = logging.getLogger()
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
        logging.basicConfig(format='[%(levelname)s][%(asctime)s]: %(message)s',level=logging.INFO)

        self.s3 = LocalCachedS3Storage(self.APP_BUCKET, os.environ.get('FINE_CACHE_ENABLED', False))

    def __ticker_access(self):
        if self.__taccess is None: self.__taccess = TickerDataAccess(self.s3, self.logger)
        return self.__taccess

    def __stock_access(self):
        if self.__saccess is None: self.__saccess = StockDataAccess()
        return self.__saccess

    def __twitter_access(self):
        if self.__twaccess is None:
            self.__twaccess = TwitterDataAccess(self.s3, self.logger,
                os.environ.get('FINE_TWEETER_CONSUMER_KEY', ''),
                os.environ.get('FINE_TWEETER_CONSUMER_SECRET', ''),
                os.environ.get('FINE_TWEETER_ACCESS_TOKEN', ''),
                os.environ.get('FINE_TWEETER_ACCESS_SECRET', ''))
        return self.__twaccess

    def load_stocks(self, symbol):
        return self.__stock_access().load_all() if symbol is None else self.__stock_access().load_one(symbol)

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
        return Simulator(self.logger, self.__ticker_access()).simulate(signal)

    def load_tickers(self, stock):
        return self.__ticker_access().load(stock.symbol, Ticker.Type.ONE_DAY)

    def update(self, symbols, type, period, limit):
        if not symbols: symbols = self.__ticker_access().symbols2update(type, limit)
        return self.__ticker_access().update(symbols, type, period)

    def twitter_update(self):
        self.__twitter_access().update_all()

    def extterms(self, date):
        return SentimentAnalyzer(self.__twitter_access()).extract_terms(date)

def lambda_ticker_1h_update(event, context):
    # needs ~1h40mins to complete all
    app = AppContext()
    for i in range(0, 100):
        app.logger.info(f"iteration {i}")
        if not app.update(None, Ticker.Type.ONE_HOUR, 1, 2): break
    return {'resultCode': 200}

def lambda_ticker_5m_update(event, context):
    # needs ~2h to complete all
    app = AppContext()
    for i in range(0, 10):
        app.logger.info(f"iteration {i}")
        if not app.update(None, Ticker.Type.FIVE_MIN, 1, 16): break
    return {'resultCode': 200}

def lambda_ticker_1m_update(event, context):
    app = AppContext()
    # needs ~4h40m to complete all
    for i in range(0, 10):
        app.logger.info(f"iteration {i}")
        if not app.update(None, Ticker.Type.ONE_MIN, 1, 7): break
    return {'resultCode': 200}

def lambda_ticker_opts_update(event, context):
    app = AppContext()
    # needs ~4h40m to complete all
    for i in range(0, 10):
        app.logger.info(f"iteration {i}")
        if not app.update(None, Ticker.Type.OPTIONS, 1, 7): break
    return {'resultCode': 200}

def lambda_ticker_1d_update(event, context):
    app = AppContext()
    # needs ~4h40m to complete all
    for i in range(0, 10):
        app.logger.info(f"iteration {i}")
        if not app.update(None, Ticker.Type.ONE_DAY, 'max', 7): break
    return {'resultCode': 200}

def lambda_twitter_update(event, context):
    app = AppContext()
    app.logger.info("started twitter update")
    app.twitter_update()
    app.logger.info("finished twitter update")
    return {'resultCode': 200}

APPLOGIC_LAMBDA_NAMES = ["update_twitter", "update_options", "update_5m_tickers",
    "update_1d_tickers", "update_1h_tickers", "update_1m_tickers"]

def lambda_finalize_deployment(event, context):
    app = AppContext()
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    if bucket == app.APP_BUILDS and key == app.APP_PKG_NAME:
        app.logger.info(f"triggeed deplyment for {bucket}:{key}")
        client = boto3.client('lambda')
        for fname in APPLOGIC_LAMBDA_NAMES:
            client.update_function_code(FunctionName=fname, S3Bucket=bucket, S3Key=key)
            app.logger.info(f"finished deplyment for {fname}")

    app.logger.info("finished all deplyments.")
    return {'resultCode': 200}
