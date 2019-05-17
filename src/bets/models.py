
class Bet:
    # types
    TYPE_STOCK = "STOCK"
    TYPE_OPTION = "OPTION"

    # statuses
    STATUS_ACTIVE = "active"
    STATUS_SUCCESS = "success"
    STATUS_FAILURE = "failure"

    def __init__(self, name, type, stock, description,
                 buy_price, buy_time, sell_price, sell_time,
                 exit_negative_price, exit_positive_price,
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
        self.status = status
        self.status_reason = status_reason
