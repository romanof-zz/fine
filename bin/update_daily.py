from config import CONFIG
from tickers.data_access import TickerDataAccess

TickerDataAccess(CONFIG.root, CONFIG.secrets["yahoo"]["token"], CONFIG.secrets["yahoo"]["auth_cookie"]).update(CONFIG.stocks)
