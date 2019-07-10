import yaml
import argparse
import sys
from datetime import datetime, timedelta

from app import AppContext
from util import valid_date

parser = argparse.ArgumentParser()

# analysis params
parser.add_argument("-t", "--threshold", type=float, default=0.8, help="threshold to use for bets")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
parser.add_argument("--no-simulate", dest="simulate", default=True, action="store_false", help="simulate created bets")

# stock data set
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("--today", default=False, action="store_true", help="consider only stocks updated today")

# timeframe limits
parser.add_argument("-d", "--date", type=valid_date, help="run analysis with a given date as a start date")
parser.add_argument("-i", "--interval", type=int, default=1, help="run analysis for a given interval from a date")

args = parser.parse_args()

APP = AppContext()

stocks = APP.load_stocks(args.stock, args.today)

signals = []
for idx, stock in enumerate(stocks):
    tickers = APP.load_tickers(stock)
    time = args.date if args.date is not None else datetime.today()
    for d in range(0, args.interval):
        signal = APP.analyze(list(filter(lambda t: t.time <= time - timedelta(days=d), tickers)),
            args.period, args.function, args.threshold)
        if signal: signals.append(signal)
    print("processed {} of {} stocks.".format(idx, len(stocks)))

if args.simulate: [APP.simulate(signal) for signal in signals]

APP.logger.info("signals (total={}):\n{}".format(len(signals), yaml.dump(signals)))
