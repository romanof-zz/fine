import yaml
import argparse
from app import APP

from stocks.analyzers import TickerAnalyzer
from bets.models import Bet

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

threshold = float(APP.secrets["ticker"]["analysis_threshold"])
if args.stock is not None:
    stocks = [APP.stock_access.load_one(args.stock)]
else:
    stocks = APP.stock_access.all_updated_today()

with open("bets.yml", "w+") as file:
    for stock in stocks:
        tickers = APP.ticker_access.load([stock])
        results = TickerAnalyzer(tickers, APP.logger).analyze(args.period, args.function)

        bets = []
        for result in results:
            for stat in result.to_stats_above_chance_value(threshold):
                if stat: bets.append(Bet.from_ticker_stats(stat))

        if bets: file.write(yaml.dump(bets))
