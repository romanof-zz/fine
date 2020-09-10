import operator

from datetime import timedelta, datetime
from botocore.exceptions import ClientError
from .models import Bet
from .access import BetDataAccess
from util import DATE_FORMAT
from stocks.models import Ticker, TickerAnalysisStats

class BetProcessor:
    RISK_DIVIATION = .3

    def __init__(self, logger, ticker_access):
        self.logger = logger
        self.ticker_access = ticker_access

    def check_ticker(self, bet, ticker):
        # target
        if bet.status == Bet.Status.UNKNOWN and (
          (bet.type == Bet.Type.BUY and bet.target_price <= ticker.high) or
          (bet.type == Bet.Type.SELL and bet.target_price >= ticker.low)):
            bet.status = Bet.Status.SUCCESS
            return True

        # limit
        if bet.status == Bet.Status.UNKNOWN and (
          (bet.type == bet.Type.BUY and bet.limit_price >= ticker.low) or
          (bet.type == bet.Type.SELL and bet.limit_price <= ticker.high)):
            bet.status = Bet.Status.FAILURE
            return True

        return False

    @classmethod
    def bet_from_ticker_stat(self, tstat, invert=False):
        # init reusable vars
        curr_price = tstat.ticker_result.current.close
        curr_time = tstat.ticker_result.current.time

        # determine signal type
        type = Bet.Type.BUY if tstat.type == TickerAnalysisStats.Type.UP and not invert else Bet.Type.SELL

        # determine operators
        target_operator = "add" if type == Bet.Type.BUY else "sub"
        limit_operator = "sub" if type == Bet.Type.BUY else "add"

        # determine ratios
        target_ratio = getattr(operator, target_operator)(1, tstat.percent_change)
        limit_ratio = getattr(operator, limit_operator)(1, tstat.percent_change * self.RISK_DIVIATION)

        # generating signal
        return Bet(tstat.ticker_result.symbol, type,
                      "[ticker_analyser][{stock} : {price}][{type}] change: {change:.2f}% in {frame} trading days, after hitting {period}d {function} with {percent:.2f}% chance ({event_cnt} events).".format(
                        stock=tstat.ticker_result.symbol,
                        price=curr_price,
                        type=type,
                        change=tstat.percent_change * 100,
                        frame=tstat.result_frame,
                        period=tstat.ticker_result.period,
                        function=tstat.ticker_result.function,
                        percent=tstat.chance * 100,
                        event_cnt=tstat.count),
                   # event data
                   curr_time,
                   curr_price,
                   # target data
                   curr_time + timedelta(days=tstat.result_frame),
                   round(curr_price * target_ratio, 2),
                   # limit
                   round(curr_price * limit_ratio, 2));

    def check_bet(self, bet):
        trading_days = days = 1
        while(True):
            try:
                # start simulation from next morning after event
                time = bet.event_time + timedelta(days=days)
                tickers = self.ticker_access.load(bet.symbol,
                                                  Ticker.Type.FIVE_MIN,
                                                  time.strftime(DATE_FORMAT))
                self.logger.info(f"simulating {bet.symbol} on {time.strftime(DATE_FORMAT)} with {len(tickers)} tickers")

                # check ticker for exit conditions
                for ticker in tickers:
                    if self.check_ticker(bet, ticker):
                        return True

                # check expiration
                if time >= bet.target_time:
                    bet.status = Bet.Status.EXPIRED
                    return True

            except ClientError:
                self.logger.error(f"failed to load {bet.symbol} on {time.strftime(DATE_FORMAT)}")
                if time > datetime.now(): return False

            finally:
                days+=1

class BetsController:
    def __init__(self, access):
        self.access = access

    def all(self):
        return self.access.load_all()
