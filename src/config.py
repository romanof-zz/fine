import yaml
import os.path

class Config:
    def __init__(self):
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        self.stocks = [
          "AMZN", "GOOG", "AAPL", "FB", "NFLX", "MSFT", # tech
          "LRCX","UNH", "BHGE", "ATVI", "ALK", "AXP", "JNJ" # random
        ]

        with open("{dir}/secrets.yaml".format(dir=self.root), 'r') as file:
             self.secrets = yaml.load(file, Loader=yaml.BaseLoader)

CONFIG = Config()
