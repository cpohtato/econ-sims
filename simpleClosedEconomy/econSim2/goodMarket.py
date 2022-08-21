from .pop import *
from .firm import *

class Stall():
    def __init__(self):
        pass

class GoodMarket():
    def __init__(self, goodType: int, initPrice: float):
        self.goodType: int = goodType

        self.prevAvgPrice: float = initPrice

    def getPrevAvgPrice(self):
        return self.prevAvgPrice

    def placeGoods(self, firmID)