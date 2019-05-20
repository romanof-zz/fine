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

    def __init__(self, name, type, stock, description,
                 buy_price, buy_time, sell_price, sell_time,
                 exit_negative_price, exit_positive_price, expiration_time,
                 status, status_reason):
        self.name = name
        self.type = type
        self.stock = stock
        self.description = description
        self.buy_price = buy_price
        self.buy_time = buy_time
        self.sell_price = sell_price
        self.sell_time = sell_time
        self.exit_negative_price = exit_negative_price
        self.exit_positive_price = exit_positive_price
        self.expiration_time = expiration_time
        self.status = status
        self.status_reason = status_reason

    @classmethod
    def from_ticker_stats(self, stat):
        return Bet("[ticker_analyser]: [{stock} : {price}] - {dir} {change:.2f}%".format(
                        stock=stat.ticker_result.stock,
                        price=stat.ticker_result.current.adj_close,
                        dir=stat.type,
                        change=stat.percent_change * 100),
                   self.TYPE_STOCK, stat.ticker_result.stock,
                   "[{stock} : {price}] might go {dir} by {change:.2f}% in {frame} days, after hitting {period}d {function} with {percent:.2f}% chance".format(
                       stock=stat.ticker_result.stock,
                       price=stat.ticker_result.current.adj_close,
                       dir=stat.type,
                       change=stat.percent_change * 100,
                       frame=stat.result_frame,
                       period=stat.ticker_result.period,
                       function=stat.ticker_result.function,
                       percent=stat.chance * 100),
                   None, None, None, None,
                   round(stat.ticker_result.current.adj_close * (1 - stat.percent_change / self.BET_RATIO), 2),
                   round(stat.ticker_result.current.adj_close * (1 + stat.percent_change), 2),
                   datetime.datetime.now() + datetime.timedelta(days=stat.result_frame),
                   self.STATUS_ACTIVE, None);
