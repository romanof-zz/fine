import yaml
from .models import Bet

class BetsDataAccess:
    S3_BUCKET = "fine.bets"

    ACTIVE = "active.yml"
    ARCHIVE = "archive.yml"

    def __init__(self, store):
        self.store = store.with_bucket(self.S3_BUCKET)

    def save(self, bets, upload=False):
        self.store.put(self.ACTIVE, yaml.dump(bets).encode(), upload)
        if upload: self.store.upload(self.ARCHIVE)

    def load(self):
        file = self.store.get(self.ACTIVE)
        bets = yaml.load(file.read(), Loader=yaml.FullLoader)
        file.close()
        return [] if bets is None else bets
