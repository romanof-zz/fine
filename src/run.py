# /usr/local/bin/python3

import argparse
import os.path

from helpers.ticker_parser import TickerParser

ROOT = path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--stock", help="stock to analize")
args = parser.parse_args()

tickers = TickerParser(ROOT).parse_daily(args.stock)
