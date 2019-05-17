import argparse
from config import CONFIG

from tickers.analyzers import TickerAnalyzer
from tickers.data_access import TickerDataAccess
from storage.s3_cached_store import S3CachedStore

access = TickerDataAccess(S3CachedStore(CONFIG.root),
                          CONFIG.secrets["yahoo"]["token"],
                          CONFIG.secrets["yahoo"]["auth_cookie"])

parser = argparse.ArgumentParser()
parser.add_argument('--no-update', dest='update', default=True, action='store_false')
parser.add_argument('--no-analyze', dest='analyze', default=True, action='store_false')

parser.add_argument("-s", "--stock", help="stock to analize")
parser.add_argument("-p", "--period", help="analysis period")
parser.add_argument("-f", "--function", help="analysis function")
args = parser.parse_args()

stocks = CONFIG.stocks if args.stock is None else [args.stock]
if args.update: access.update(stocks)
if args.analyze:
    threshold = float(CONFIG.secrets["ticker"]["analysis_threshold"])
    tickers = access.load(stocks)
    results = TickerAnalyzer(tickers).analyze(args.period, args.function)
    stats = list( filter(lambda s: s, map(lambda r: r.to_stats_above_chance_value(threshold), results)))
    print(len(stats))
