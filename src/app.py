import yaml
import logging
import os.path
from storage import S3Storage, SQLStorage
from stocks.data_access import StockDataAccess, TickerDataAccess

class AppContext:
    APP_BUCKET = "fine.data"
    DB_NAME = 'fine'

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

        with open("{dir}/secrets.yml".format(dir=self.root), 'r') as file:
             self.secrets = yaml.load(file, Loader=yaml.BaseLoader)

        self.s3 = S3Storage(self.APP_BUCKET)
        self.sql = SQLStorage(self.logger,
                              self.secrets['rds']['host'],
                              self.secrets['rds']['user'],
                              self.secrets['rds']['password'],
                              self.DB_NAME)

        self.stock_access = StockDataAccess(self.sql)
        self.ticker_access = TickerDataAccess(self.root, self.stock_access, self.s3, self.logger,
                                              self.secrets["yahoo"]["token"],
                                              self.secrets["yahoo"]["auth_cookie"],
                                              self.secrets["aplhavantage"]["app_key"])

APP = AppContext()
