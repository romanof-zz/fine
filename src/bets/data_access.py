import yaml
from .models import Bet

class BetsDataAccess:
    S3_BUCKET_PREFIX = "fine.bets"

    def __init__(self, store):
        self.store = store.with_bucket("fine.bets")
