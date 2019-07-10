import argparse
from app import AppContext

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--update", default=False, action="store_true", help="update tweets")
args = parser.parse_args()

if args.update: AppContext().twitter_update()
