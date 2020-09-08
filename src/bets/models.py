class Bet:
    class Status:
        UNKNOWN = "unknown"
        SUCCESS = "success"
        FAILURE = "failure"
        EXPIRED = "expired"

    class Type:
        BUY = 'buy'
        SELL = 'sell'

    def __init__(self, symbol, type, info, event_time, event_price, target_time, target_price, limit_price):
        # general
        self.symbol = symbol
        self.type = type
        self.info = info
        self.status = self.Status.UNKNOWN

        # bet limits
        self.event_time = event_time
        self.event_price = event_price
        self.target_time = target_time
        self.target_price = target_price
        self.limit_price = limit_price

class Bid:
    def __init(self):
        # bid can only by placed bet
        self.bet = bet
        # user making a bid
        self.user = user
        # $ amount to bid
        self.amount = amount

        # position price and time.
        self.open_time = open_time
        self.open_price = open_price
        self.close_time = close_time
        self.close_price = close_price
