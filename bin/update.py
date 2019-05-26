import argparse
from app import APP
from stocks.data_access import TickerDataAccess
from stocks.models import Ticker

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock symbol")
parser.add_argument("-t", "--type", default="daily", help="type of ticker")
args = parser.parse_args()

if args.stock is not None:
    stocks = [APP.stock_access.load_one(args.stock)]
if args.type == Ticker.DAILY:
    if args.stock is None: stocks = APP.stock_access.load_not_updated(Ticker.DAILY)
    APP.ticker_access.update_daily(stocks)
if args.type == Ticker.INTRADAY:
    if args.stock is None: stocks = APP.stock_access.load_not_updated(Ticker.INTRADAY)
    APP.ticker_access.update_intraday(stocks)
