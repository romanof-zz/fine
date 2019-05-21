import yaml
import argparse
from app import APP

from stocks.analyzers import TickerAnalyzer
from stocks.data_access import TickerDataAccess
from bets.models import Bet

access = TickerDataAccess(APP.root, APP.s3, APP.logger,
                          APP.secrets["yahoo"]["token"],
                          APP.secrets["yahoo"]["auth_cookie"])

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

stocks = APP.stocks if args.stock is None else [args.stock]
threshold = float(APP.secrets["ticker"]["analysis_threshold"])

with open("bets.yml", "w+") as file:
    for stock in stocks:
        tickers = access.load([stock])
        results = TickerAnalyzer(tickers, APP.logger).analyze(args.period, args.function)

        bets = []
        for result in results:
            for stat in result.to_stats_above_chance_value(threshold):
                if stat: bets.append(Bet.from_ticker_stats(stat))

        if bets: file.write(yaml.dump(bets))
