import argparse
from app import APP
from stocks.data_access import TickerDataAccess

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock symbol")
parser.add_argument("-t", "--type", default="daily", help="type of ticker")
args = parser.parse_args()

stocks = APP.stocks if args.stock is None else [args.stock]

access = TickerDataAccess(APP.root, APP.s3, APP.logger,
                 APP.secrets["yahoo"]["token"],
                 APP.secrets["yahoo"]["auth_cookie"],
                 APP.secrets["aplhavantage"]["app_key"])

if args.type == "daily":
    access.update_daily(stocks)
if args.type == "intraday":
    access.update_intraday(stocks)
