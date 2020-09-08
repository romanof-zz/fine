import yaml
import argparse
import sys
import concurrent.futures
from datetime import datetime

from bets.models import Signal
from app import AppContext
from util import valid_date

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--threshold", type=float, default=0.6, help="threshold to use for bets")
parser.add_argument("-f", "--frame", type=int, help="result frame")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-fn", "--function", help="analysis function")
parser.add_argument("--no-simulate", dest="simulate", default=True, action="store_false", help="simulate created bets")
parser.add_argument("--inv", dest="invert", default=False, action="store_true", help="invert reaction")
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-d", "--date", type=valid_date, help="run analysis with a given date as a start date")
parser.add_argument("-i", "--interval", type=int, default=1, help="run analysis for a given interval from a date")
args = parser.parse_args()

APP = AppContext()

date = args.date if args.date is not None else datetime.today()
stocks = APP.load_stocks(args.stock)
signals = []

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    future_to_signals = {executor.submit(APP.analyze_timeframe,
        stock, args.period, args.function, args.threshold, date, args.interval, args.frame, args.invert):
        stock.symbol for stock in stocks}
    for future in concurrent.futures.as_completed(future_to_signals): signals += future.result()

if args.simulate:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        [executor.submit(APP.simulate, signal) for signal in signals]

APP.logger.info(yaml.dump(signals))
APP.logger.info("total {}".format(len(signals)))
APP.logger.info("unknown {}".format(len(list(filter(lambda s: s.exit_status == Signal.Status.UNKNOWN, signals)))))
APP.logger.info("success {}".format(len(list(filter(lambda s: s.exit_status == Signal.Status.SUCCESS, signals)))))
APP.logger.info("failure {}".format(len(list(filter(lambda s: s.exit_status == Signal.Status.FAILURE, signals)))))
APP.logger.info("expired {}".format(len(list(filter(lambda s: s.exit_status == Signal.Status.EXPIRED, signals)))))
