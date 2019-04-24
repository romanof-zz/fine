import argparse
import os.path
import sys

from ticker.helpers import TickerConfig
from ticker.analyzers import TickerAnalyzer

CONFIG = TickerConfig(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

parser = argparse.ArgumentParser()
parser.add_argument('--no-update', dest='update', default=True, action='store_false')
parser.add_argument('--no-analyze', dest='analyze', default=True, action='store_false')

parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

stocks = CONFIG.default_stocks() if args.stock is None else [args.stock]
if args.update: CONFIG.updater(stocks).update_daily()
if not args.analyze: sys.exit(0)

tickers = CONFIG.parser().parse_daily(stocks)
analyzer = TickerAnalyzer(tickers)
analyzer.analyze(args.period, args.function)
