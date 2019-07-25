import argparse
from datetime import datetime

# time formatting
DATE_FORMAT = '%Y-%m-%d'

# args date validation
def valid_date(s):
    try:
        return datetime.strptime(s, DATE_FORMAT)
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
