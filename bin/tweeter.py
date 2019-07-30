import argparse
from app import AppContext

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--update", default=False, action="store_true", help="update tweets")
parser.add_argument("-t", "--terms", default=False, action="store_true")
parser.add_argument("-d", "--date")
args = parser.parse_args()

if args.update: AppContext().twitter_update()
if args.terms: print(AppContext().extterms(args.date))
