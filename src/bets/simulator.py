from datetime import timedelta
from botocore.exceptions import ClientError
from .models import Bet

class BetSimulator:
    def __init__(self, logger, ticker_access):
        self.logger = logger
        self.ticker_access = ticker_access

    def simulate(self, bet):
        time = bet.event_time
        err_cnt = 0
        while(True):
            try:
                # start simulation from next morning after event
                time += timedelta(days=1)
                tickers = self.ticker_access.load_intraday(bet.stock, time)
                err_cnt = 0
                self.logger.info("simulating {s} on {t} with {c} tickers".format(
                    s=bet.stock.symbol,
                    t=time,
                    c=len(tickers)))
                for ticker in tickers:
                    bet.update(ticker)
                    if bet.status != Bet.STATUS_ACTIVE:
                        return True
            except ClientError:
                self.logger.error("failed to load {s} on {t}".format(s=bet.stock.symbol, t=time))
                err_cnt+=1
                if err_cnt>3: return False
