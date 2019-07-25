import argparse
from app import AppContext
from stocks.models import Ticker

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stocks")
parser.add_argument("-l", "--limit", type=int, default=100)
parser.add_argument("-t", "--type", default=Ticker.Type.ONE_MIN, choices=Ticker.TYPES)
parser.add_argument("-p", "--period", type=int, default=1)
args = parser.parse_args()

# always load all data for 1d intervals
period = 'max' if args.type == Ticker.Type.ONE_DAY else args.period
# split stocks before updating
stocks = args.stocks.split() if args.stocks else []

AppContext().update(stocks, args.type, period, args.limit)
