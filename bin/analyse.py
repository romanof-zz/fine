import yaml
import argparse
from config import CONFIG

from tickers.analyzers import TickerAnalyzer
from tickers.data_access import TickerDataAccess
from bets.models import Bet

access = TickerDataAccess(CONFIG.root,
                          CONFIG.secrets["yahoo"]["token"],
                          CONFIG.secrets["yahoo"]["auth_cookie"])

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

stocks = CONFIG.stocks if args.stock is None else [args.stock]

threshold = float(CONFIG.secrets["ticker"]["analysis_threshold"])
tickers = access.load(stocks)
results = TickerAnalyzer(tickers).analyze(args.period, args.function)

bets = []
for result in results:
    for stat in result.to_stats_above_chance_value(threshold):
        if stat: bets.append(Bet.from_ticker_stats(stat))

print("====== START OUTPUT ========")
print(yaml.dump(bets))
print("====== END OUTPUT ========")
