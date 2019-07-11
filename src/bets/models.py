import datetime
import operator
from stocks.models import TickerAnalysisStats

class Signal:
    RISK_DIVIATION = .3

    class Status:
        UNKNOWN = "unknown"
        SUCCESS = "success"
        FAILURE = "failure"
        EXPIRED = "expired"

    def __init__(self, stock, type, info, event_time, event_price, target_price, risk_price, ttl):
        # general data
        self.stock = stock
        self.type = type
        self.info = info
        self.event_time = event_time
        self.event_price = event_price

        # bet limits
        self.target_price = target_price
        self.risk_price = risk_price
        self.ttl = ttl

        # state tracking
        self.exit_status = self.Status.UNKNOWN
        self.exit_time = None
        self.exit_price = None

    @classmethod
    def from_ticker_stat(self, tstat):
        # init reusable vars
        curr_price = tstat.ticker_result.current.adj_close
        curr_time = tstat.ticker_result.current.time
        # determine operators
        target_operator = "add" if tstat.type == TickerAnalysisStats.UP  else "sub"
        risk_operator = "sub" if tstat.type == TickerAnalysisStats.UP  else "add"
        # determine ratios
        target_ratio = getattr(operator, target_operator)(1, tstat.percent_change)
        risk_ratio = getattr(operator, risk_operator)(1, tstat.percent_change * self.RISK_DIVIATION)
        # generating signal
        return Signal(tstat.ticker_result.stock, tstat.type,
                      "[ticker_analyser][{stock} : {price}] might go {dir} by {change:.2f}% in {frame} trading days, after hitting {period}d {function} with {percent:.2f}% chance ({event_cnt} events).".format(
                        stock=tstat.ticker_result.stock.symbol,
                        price=curr_price,
                        dir=tstat.type,
                        change=tstat.percent_change * 100,
                        frame=tstat.result_frame,
                        period=tstat.ticker_result.period,
                        function=tstat.ticker_result.function,
                        percent=tstat.chance * 100,
                        event_cnt=tstat.count),
                   curr_time, curr_price,
                   round(curr_price * target_ratio, 2), round(curr_price * risk_ratio, 2), tstat.result_frame);

    def check_ticker(self, ticker):
        # target
        if self.exit_status == self.Status.UNKNOWN and (
          (self.type == TickerAnalysisStats.UP and self.target_price <= ticker.high) or
          (self.type == TickerAnalysisStats.DOWN and self.target_price >= ticker.low)):
            self.exit_price = ticker.close
            self.exit_time = ticker.time
            self.exit_status = self.Status.SUCCESS
            return True

        # risk
        if self.exit_status == self.Status.UNKNOWN and (
          (self.type == TickerAnalysisStats.UP and self.risk_price >= ticker.low) or
          (self.type == TickerAnalysisStats.DOWN and self.risk_price <= ticker.high)):
            self.exit_price = ticker.close
            self.exit_time = ticker.time
            self.exit_status = self.Status.FAILURE
            return True

        return False
