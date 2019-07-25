from datetime import timedelta, datetime
from botocore.exceptions import ClientError
from .models import Signal
from util import DATE_FORMAT

class Simulator:
    def __init__(self, logger, ticker_access):
        self.logger = logger
        self.ticker_access = ticker_access

    def simulate(self, signal):
        trading_days = days = 1
        while(True):
            try:
                # start simulation from next morning after event
                time = signal.event_time + timedelta(days=days)
                tickers = self.ticker_access.load(signal.symbol, Ticker.Type.FIVE_MIN, time.strftime(DATE_FORMAT))
                self.logger.info("simulating {s} on {t} with {c} tickers".format(
                    s=signal.stock.symbol,
                    t=time,
                    c=len(tickers)))

                # check ticker for exit conditions
                for ticker in tickers:
                    if signal.check_ticker(ticker): return True

                # check ttl
                if trading_days == signal.ttl:
                    signal.exit_price = ticker.close
                    signal.exit_time = ticker.time
                    signal.exit_status = Signal.Status.EXPIRED
                    return True

                trading_days+=1

            except ClientError:
                self.logger.error("failed to load {s} on {t}".format(s=signal.symbol, t=time))
                if time > datetime.now(): return False

            finally:
                days+=1
