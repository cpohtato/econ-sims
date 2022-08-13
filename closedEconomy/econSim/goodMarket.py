from .labourMarket import *

class GoodMarket:
    def __init__(self, goodType, initPrice=None, initSupply=None, initSold=None, initProduced=None):
        self.goodType = goodType
        
        self.price = INIT_PRICE[goodType]
        if not (initPrice == None):
            self.price = initPrice

        self.prevSupply: int = 0
        if not (initSupply == None):
            self.prevSupply = initSupply

        self.prevSold: int = 0
        if not (initSold == None):
            self.prevSold = initSold

        self.prevProduced: int = 0
        if not (initProduced == None):
            self.prevProduced = initProduced

        self.currSupply = self.prevSupply
        self.currProduced = self.prevProduced
        self.currSold = self.prevSold

    def getPrice(self):
        return self.price

    def getAvailable(self):
        return self.currSupply - self.currSold

    def getSold(self):
        return self.currSold

    def getSupply(self):
        return self.currSupply

    def getProduced(self):
        return self.currProduced

    def setPrice(self):
        goodEquilibrium = int((1 - INVENTORY_TARGET) * self.prevSupply)
        self.price = (1 + MONTHLY_INFLATION) * self.price
        if (self.prevSold > goodEquilibrium):
            self.price = random.uniform(1, 1 + PRICE_VISCOSITY) * self.price
        elif (self.prevSold == goodEquilibrium):
            self.price = self.price
        elif (self.prevSold < goodEquilibrium):
            self.price = random.uniform(1 - PRICE_VISCOSITY, 1) * self.price

        self.price = round(self.price, 5)

    def addGoods(self, qtyProduced, qtyTotal):
        # self.currSupply += qtyTotal
        self.currSupply += qtyProduced
        self.currProduced += qtyProduced

    def registerSale(self):
        self.currSold += 1 

    def reset(self):
        self.prevSupply = self.currSupply
        self.prevProduced = self.currProduced
        self.prevSold = self.currSold

        self.currSupply = 0
        self.currProduced = 0
        self.currSold = 0

    def log(self):
        with open("closedEconomy/log/sales.txt", "a") as logFile:
            logFile.write(DICT_GOOD_NAMES[self.goodType] + " Market: " + str(self.getSold()) + "/" 
            + str(self.getSupply()) + " sold at $" + "{:.2f}".format(self.getPrice()) + "\n")