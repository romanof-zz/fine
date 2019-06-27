import datetime

class Bet:
    # types
    TYPE_STOCK = "STOCK"
    TYPE_OPTION = "OPTION"

    # statuses
    STATUS_ACTIVE = "active"
    STATUS_SUCCESS = "success"
    STATUS_FAILURE = "failure"

    BET_RATIO = 3

    def __init__(self, name, type, stock, description, event_time,
                 buy_price, buy_time, sell_price, sell_time,
                 exit_negative_price, exit_positive_price, expiration_time,
                 status, status_reason):
        # general data
        self.name = name
        self.type = type
        self.stock = stock
        self.description = description
        self.event_time = event_time

        # info about the actual bet prices
        self.buy_price = buy_price
        self.buy_time = buy_time
        self.sell_price = sell_price
        self.sell_time = sell_time

        # bet limits
        self.exit_negative_price = exit_negative_price
        self.exit_positive_price = exit_positive_price
        self.expiration_time = expiration_time

        # state tracking
        self.status = status
        self.status_reason = status_reason

    @classmethod
    def create(self, analysis_stat):
        return Bet("[ticker_analyser]: [{stock} : {price}] - {dir} {change:.2f}%".format(
                        stock=analysis_stat.ticker_result.stock.symbol,
                        price=analysis_stat.ticker_result.current.adj_close,
                        dir=analysis_stat.type,
                        change=analysis_stat.percent_change * 100),
                   self.TYPE_STOCK,
                   analysis_stat.ticker_result.stock,
                   "[{stock} : {price}] might go {dir} by {change:.2f}% in {frame} days, after hitting {period}d {function} with {percent:.2f}% chance".format(
                       stock=analysis_stat.ticker_result.stock.symbol,
                       price=analysis_stat.ticker_result.current.adj_close,
                       dir=analysis_stat.type,
                       change=analysis_stat.percent_change * 100,
                       frame=analysis_stat.result_frame,
                       period=analysis_stat.ticker_result.period,
                       function=analysis_stat.ticker_result.function,
                       percent=analysis_stat.chance * 100),
                   analysis_stat.ticker_result.current.time,
                   None, None, None, None,
                   round(analysis_stat.ticker_result.current.adj_close * (1 - analysis_stat.percent_change / self.BET_RATIO), 2),
                   round(analysis_stat.ticker_result.current.adj_close * (1 + analysis_stat.percent_change), 2),
                   analysis_stat.ticker_result.current.time + datetime.timedelta(days=analysis_stat.result_frame),
                   self.STATUS_ACTIVE, None);

    def update(self, ticker):
        # do nothing if ticker is for other stock
        if self.stock.symbol != ticker.stock.symbol: return False
        updated = False

        # buying?
        if self.buy_time == None and self.status == self.STATUS_ACTIVE:
            self.buy_time = ticker.time
            self.buy_price = ticker.open
            updated = True

        # selling happy:
        if self.status == self.STATUS_ACTIVE and self.exit_positive_price <= ticker.high:
            self.sell_time = ticker.time
            self.sell_price = ticker.close
            self.status = self.STATUS_SUCCESS
            self.status_reason = "ticker high is over expected positive exit."
            updated = True

        # selling sad:
        if self.status == self.STATUS_ACTIVE and self.exit_negative_price >= ticker.low:
            self.sell_time = ticker.time
            self.sell_price = ticker.close
            self.status = self.STATUS_FAILURE
            self.status_reason = "ticker low is under expected negative exit."
            updated = True

        # selling expired:
        if self.status == self.STATUS_ACTIVE and self.expiration_time < ticker.time:
            self.sell_time = ticker.time
            self.sell_price = ticker.close
            self.status = self.STATUS_FAILURE
            self.status_reason = "bet has expired."
            updated = True

        return updated
