import argparse
import os.path

from ticker.helpers import TickerConfig
from ticker.analyzers import TickerAnalyzer

CONFIG = TickerConfig(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

# https://query1.finance.yahoo.com/v7/finance/download/GOOG?period1=1552867736&period2=1555546136&interval=1d&events=history&crumb=6dfZ4Wz26XV

stocks = CONFIG.default_stocks() if args.stock is None else [args.stock]
tickers = CONFIG.parser().parse_daily(stocks)
analyzer = TickerAnalyzer(tickers)
analyzer.analyze(args.period, args.function)
