from app import Context
from bets.controllers import BetsController

class ApiContext(Context):

    def __init__(self):
        super().__init__()

        self.__bets__controller = None

    def __bets_controller(self):
        if self.__bets__controller is None: self.__bets__controller = BetsController(self.bet_access())
        return self.__bets__controller

    def bets_all(self):
        return self.__bets_controller().all()

def lambda_bets_all(event, context):
    return ApiContext().bets_all()
