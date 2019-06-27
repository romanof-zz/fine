from datetime import datetime
import argparse
from stocks.models import Ticker

# args date validation
def valid_date(s):
    try:
        return datetime.strptime(s, Ticker.DAILY_TIME_FORMAT)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
