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

print("total event count: {cnt}".format(cnt=res["count"]))
for offset in [1, 3, 7, 14, 30]:
    print("changes after {o} days:".format(o=offset))
    print("  higher: avg price change: {hpp:.2f}%; with events: {he} ({hep:.2f}%)".format(
      hpp=res[offset]["sum_hi_percent_change"] / res[offset]["hi_count"] * 100,
      he=res[offset]["hi_count"],
      hep=res[offset]["hi_count"] / res["count"] * 100))
    print("  lower: avg price change: {lpp:.2f}%; with events: {le} ({lep:.2f}%)".format(
      lpp=res[offset]["sum_lo_percent_change"] / res[offset]["lo_count"] * 100,
      le=res[offset]["lo_count"],
      lep=res[offset]["lo_count"] / res["count"] * 100))
