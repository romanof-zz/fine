import argparse
import os.path

from helpers.ticker_parser import TickerParser
from analyzers.ticker_analyzer import TickerAnalyzer

ROOT = path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock to analize")
args = parser.parse_args()

tickers = TickerParser(ROOT).parse_daily(args.stock)
res = TickerAnalyzer(tickers).test_52w_max_adj_close()

print("count for 52w max adj_close: {cnt}".format(cnt=res["count"]))
print("count for 52w max adj_close went under after 1d: {cnt}".format(cnt=res["count_price_under_max_1d"]))
print("count for 52w max adj_close went under after 3d: {cnt}".format(cnt=res["count_price_under_max_3d"]))
print("count for 52w max adj_close went under after 7d: {cnt}".format(cnt=res["count_price_under_max_7d"]))
