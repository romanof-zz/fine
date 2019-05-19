import argparse
from config import CONFIG

from tickers.analyzers import TickerAnalyzer
from tickers.data_access import TickerDataAccess
from bets.data_access import BetsDataAccess
from bets.models import Bet
from storage.s3_cached_store import S3CachedStore

bets_access = BetsDataAccess(S3CachedStore(CONFIG.root))
ticker_access = TickerDataAccess(S3CachedStore(CONFIG.root),
                                 CONFIG.secrets["yahoo"]["token"],
                                 CONFIG.secrets["yahoo"]["auth_cookie"])

parser = argparse.ArgumentParser()
parser.add_argument('--no-update', dest='update', default=True, action='store_false')
parser.add_argument('--no-analyze', dest='analyze', default=True, action='store_false')
parser.add_argument('--upload', dest='upload', default=False, action='store_true')

parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

stocks = CONFIG.stocks if args.stock is None else [args.stock]
bets = bets_access.load()

if args.update and not args.upload: ticker_access.update(stocks)
if args.analyze and not args.upload:
    threshold = float(CONFIG.secrets["ticker"]["analysis_threshold"])
    tickers = ticker_access.load(stocks)
    results = TickerAnalyzer(tickers).analyze(args.period, args.function)
    for result in results:
        for stat in result.to_stats_above_chance_value(threshold):
            if stat: bets.append(Bet.from_ticker_stats(stat))
    bets_access.save(bets)

if args.upload: bets_access.save(bets, True)
