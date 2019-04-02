import argparse
import os.path

from ticker.parsers import TickerParser
from ticker.analyzers import TickerAnalyzer

ROOT = path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-d", "--data", help="data to analize")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

tickers = TickerParser(ROOT).parse_daily(args.stock)
analyzer = TickerAnalyzer(tickers)
analyzer.analyze(args.data, args.period, args.function)
print(str(analyzer.result))
