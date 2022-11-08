from .pop import *
from .firm import *

class Stall():
    def __init__(self, firmID: int, price: float, qty: int = 0):
        self.firmID: int = firmID
        self.qty = qty
        self.price = price
        self.funds = 0
        self.sales = 0

    def buy(self):
        if (self.qty <= 0):
            print("Error: stall has no goods to sell")
        else:
            self.qty -= 1
            self.sales += 1
            self.funds += self.price

    def reset(self):
        self.sales = 0
        self.funds = 0


class GoodMarket():
    def __init__(self, goodType: int, initPrice: float):
        self.goodType: int = goodType
        self.listStalls: list[Stall] = []

        self.prevAvgPrice: float = initPrice
        self.prevSales: int = 0
        self.prevSupply: int = 0

    def getPrevAvgPrice(self):
        return self.prevAvgPrice

    def placeGoods(self, firmID, goodQty, goodPrice):
        foundStall: bool = False
        for stall in self.listStalls:
            if (stall.firmID == firmID):
                foundStall = True
                stall.qty += goodQty
                stall.price = goodPrice

        if not foundStall:
            self.listStalls.append(Stall(firmID, goodPrice, goodQty))

    def findLowest(self):
        lowestPrice = None
        for stall in self.listStalls:
            if (stall.qty > 0):
                if (lowestPrice == None):
                    lowestPrice = stall.price
                elif (stall.price < lowestPrice):
                    lowestPrice = stall.price

        if (lowestPrice == None):
            return -1
        else:
            return lowestPrice

    def buyLowest(self):
        lowestPrice = None
        lowestPriceID = None
        for stall in self.listStalls:
            if (stall.qty > 0):
                if (lowestPrice == None):
                    lowestPrice = stall.price
                    lowestPriceID = stall.firmID
                elif (stall.price < lowestPrice):
                    lowestPrice = stall.price
                    lowestPriceID = stall.firmID

        for stall in self.listStalls:
            if (stall.firmID == lowestPriceID):
                stall.buy()

    def reset(self):
        self.prevAvgPrice = 0
        self.prevSales = 0
        self.prevSupply = 0

        for stall in self.listStalls:
            self.prevSales += stall.sales
            self.prevAvgPrice += stall.sales * stall.price
            self.prevSupply += stall.qty + stall.sales
            stall.reset()

        if (self.prevSales > 0):
            self.prevAvgPrice /= self.prevSales
        else:
            if (self.prevSupply > 0):
                self.prevAvgPrice /= self.prevSupply
            else:
                self.prevAvgPrice = 0

    def log(self):
        with open("log/sales.txt", "a") as logFile:
            logFile.write(DICT_GOOD_NAMES[self.goodType] + " Market: " + str(self.prevSales) + "/" 
            + str(self.prevSupply) + " sold at $" + "{:.2f}".format(self.prevAvgPrice) + "\n")