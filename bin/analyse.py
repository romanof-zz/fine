import yaml
import argparse
from app import AppContext

from stocks.analyzers import TickerAnalyzer
from bets.models import Bet

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--threshold", default=0.8, help="threshold to use for bets")
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

APP = AppContext()

threshold = float(args.threshold)
stocks = [APP.stock_access.load_one(args.stock)] if args.stock is not None else APP.stock_access.load_updated_today()

with open("bets.yml", "w+") as file:
    for stock in stocks:
        tickers = APP.ticker_access.load([stock])
        results = TickerAnalyzer(tickers, APP.logger).analyze(args.period, args.function)

        bets = []
        for result in results:
            for stat in result.to_stats_above_chance_value(threshold):
                if stat: bets.append(Bet.from_ticker_stats(stat))

        if bets: file.write(yaml.dump(bets))
