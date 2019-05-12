import sys
import argparse
from config import CONFIG

from ticker.analyzers import TickerAnalyzer
from ticker.helpers import TickerUpdater, TickerParser

parser = argparse.ArgumentParser()
parser.add_argument('--no-update', dest='update', default=True, action='store_false')
parser.add_argument('--no-analyze', dest='analyze', default=True, action='store_false')

parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

stocks = CONFIG.stocks if args.stock is None else [args.stock]
updater = TickerUpdater(
    CONFIG.root,
    stocks,
    CONFIG.secrets["updater"]["token"],
    CONFIG.secrets["updater"]["auth_cookie"])

if args.update: updater.update_daily()
if not args.analyze: sys.exit(0)

tickers = TickerParser(CONFIG.root).parse_daily(stocks)
analyzer = TickerAnalyzer(tickers)
analyzer.analyze(args.period, args.function)
