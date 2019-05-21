import yaml
import logging
import os.path
from storage import S3Storage
from stocks.data_access import StockDataAccess

class AppContext:
    APP_BUCKET = "fine.data"

    def __init__(self):
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        self.s3 = S3Storage(self.APP_BUCKET)
        self.stocks = map(lambda s: s.symbol, StockDataAccess(self.s3).load())

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        with open("{dir}/secrets.yml".format(dir=self.root), 'r') as file:
             self.secrets = yaml.load(file, Loader=yaml.BaseLoader)

APP = AppContext()
