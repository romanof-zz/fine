from datetime import timedelta, datetime
from botocore.exceptions import ClientError
from .models import Signal

class Simulator:
    def __init__(self, logger, ticker_access):
        self.logger = logger
        self.ticker_access = ticker_access

    def simulate(self, signal):
        time = signal.event_time
        while(True):
            try:
                # start simulation from next morning after event
                time += timedelta(days=1)
                tickers = self.ticker_access.load_intraday(signal.stock, time)
                err_cnt = 0
                self.logger.info("simulating {s} on {t} with {c} tickers".format(
                    s=signal.stock.symbol,
                    t=time,
                    c=len(tickers)))
                for ticker in tickers:
                    signal.update(ticker)
                    if signal.exit_status != Signal.Status.UNKNOWN:
                        return True
            except ClientError:
                self.logger.error("failed to load {s} on {t}".format(s=signal.stock.symbol, t=time))
                if time > datetime.now(): return False
