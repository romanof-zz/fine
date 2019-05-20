import yaml
from .models import Bet

class BetsDataAccess:
    ACTIVE_KEY = "bets/active.yml"

    def __init__(self, store):
        self.store = store

    def load(self):
        bets = yaml.load(self.store.get(self.ACTIVE_KEY), Loader=yaml.FullLoader)
        return [] if bets is None else bets
