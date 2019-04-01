import argparse
import os.path

from helpers.ticker_parser import TickerParser
from analyzers.ticker_analyzer import TickerAnalyzer

ROOT = path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-d", "--data", help="data to analize")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

tickers = TickerParser(ROOT).parse_daily(args.stock)
res = TickerAnalyzer(tickers).analyze(args.data, args.period, args.function)

print("count: {cnt}".format(cnt=res["count"]))
print("count rebound after 1d: {cnt}".format(cnt=res["count_rebound_1d"]))
print("count rebound after 3d: {cnt}".format(cnt=res["count_rebound_3d"]))
print("count rebound after 7d: {cnt}".format(cnt=res["count_rebound_7d"]))
