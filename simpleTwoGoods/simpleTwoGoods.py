#   Two good market simulation - guns and butter
#   Discrete buyers and sellers with sell orders
#   Consumers try to maximise utility according to utility function
#   Two rounds of purchasing - one for necessities and another to maximise utility
#
#   1. Each seller uses capital to restock inventory. For each seller,
#      order = (units sold last round) + (target inventory - current inventory)**surplusCompensation
#      cost = order * costPerUnit
#
#   2. Each seller decides on a price to offer goods; if inventory above target, decrease price; otherwise increase price
#      Price can never be below cost
#
#   3. Each seller submits a sell order to the market
#      Goods are 'handed over' to market with price attached
#      Market gives sellers money as soon as transaction is made
#
#   4. Consumers receive money
#
#   5. First round of purchases: each consumer (random order) purchases a small number of necessary goods if possible
#      Buy order is automatically matched with lowest offer price available
#
#   6. Each consumer (random order) now maximises utility per dollar according to marginal utility function
#      Consumers buy one unit at a time of the good that has the highest marginal utility until funds are depleted
#
#   7. Market returns unsold goods to inventory
#
#   8. Sellers calculate profit
#
#   9. Round ends

from gettext import GNUTranslations
from operator import inv
import matplotlib.pyplot as plt
import numpy as np
import random
import math

SIM_LENGTH = 100
NUM_TYPES = 2

SELLER_SURPLUS_COMPENSATION = 1.01
PRICE_STICKINESS = 0.2
BUTTER_SUBSISTENCE = 5
INIT_GOVT_GUNS = 20
INIT_GOVT_BUTTER = 10

NUM_BUTTER_SELLERS = 5
BUTTER_UNIT_COST = 0.5
BUTTER_INIT_INV = 50
BUTTER_TARGET_INV = 50
BUTTER_INIT_PRICE = 1

NUM_GUN_SELLERS = 5
GUN_UNIT_COST = 2
GUN_INIT_INV = 20
GUN_TARGET_INV = 20
GUN_INIT_PRICE = 2.5

NUM_CONSUMERS = 20
DAILY_BUDGET = 10


class SellOrder:
    def __init__(self, type, sellerID, quantity, price):
        self.type = type
        self.sellerID = sellerID
        self.quantity = quantity
        self.price = price


class Seller:
    def __init__(self, ID, type, costPerUnit, inv, targetInv, surplusCompensation, price, previousSales = 0):
        self.ID = ID
        self.type = type
        self.costPerUnit = costPerUnit
        self.inv = inv
        self.targetInv = targetInv
        self.surplusCompensation = surplusCompensation
        self.price = price
        self.previousSales = 0
        self.expenses = 0
        self.revenue = 0
        self.sales = previousSales

    def restock(self):
        surplus = self.targetInv - self.inv
        
        if (surplus > 0):
            order = self.previousSales + int((surplus/abs(surplus)) * abs(surplus)**self.surplusCompensation)
        elif (surplus == 0):
            order = self.previousSales
        elif (surplus < 0):
            order = self.previousSales + int(-(abs(surplus)**self.surplusCompensation))

        if (order < 0):
            order = 0
        elif (order > 0):
            #   Supply throttling
            if (self.type == "butter"):
                order = int((1 - (2/math.pi) * math.atan(order/100)) * order)
            elif (self.type == "gun"):
                order = int((1 - (2/math.pi) * math.atan(order/50)) * order)

        self.inv += order
        self.expenses += order * self.costPerUnit

    def priceGoods(self):
        surplus = self.inv - self.targetInv

        # changeFactor = surplus/self.targetInv
        # if (changeFactor > 1):
        #     changeFactor = 1
        # elif (changeFactor < -1):
        #     changeFactor = -1

        if (surplus > 0):
            self.price *= random.uniform(1 - PRICE_STICKINESS, 1)
        else:
            self.price *= random.uniform(1, 1 + PRICE_STICKINESS)

        self.price = round(self.price, 2)

        if (self.price < self.costPerUnit):
            self.price = self.costPerUnit

    def reset(self):
        self.expenses = 0
        self.revenue = 0
        self.previousSales = self.sales
        self.sales = 0

    def findProfit(self):
        return self.revenue - self.expenses

    def placeSellOrder(self):
        myOrder = SellOrder(self.type, self.ID, self.inv, self.price)
        self.sales = self.inv
        self.inv = 0
        return myOrder

    def cancelSellOrder(self, quantity):
        self.inv += quantity
        self.sales -= quantity

    def makeSale(self, quantity, price):
        self.sales += quantity
        self.revenue += quantity * price


class Market:
    def __init__(self, type, numSellers,):
        self.type = type
        self.numSellers = numSellers
        self.listSellers = self.createSellerList(numSellers)
        self.listSellOrders = []
        self.dailyRevenue = 0
        self.dailySales = 0

    def createSellerList(self, numSellers):
        listSellers = []  

        if (self.type == "butter"):
            for i in range(0, numSellers):
                listSellers.append(Seller(i, self.type, BUTTER_UNIT_COST, BUTTER_INIT_INV, BUTTER_TARGET_INV, 
                SELLER_SURPLUS_COMPENSATION, BUTTER_INIT_PRICE, 10))
        elif (self.type == "gun"):
            for i in range(0, numSellers):
                listSellers.append(Seller(i, self.type, GUN_UNIT_COST, GUN_INIT_INV, GUN_TARGET_INV, 
                SELLER_SURPLUS_COMPENSATION, GUN_INIT_PRICE, 2))

        return listSellers

    def addSellOrder(self, newOrder):
        self.listSellOrders.append(newOrder)

    def findLowest(self):
        #   Return lowest price and ID of corresponding sell order

        if (self.listSellOrders):
            #   Sell order list is not empty
            lowestPrice = self.listSellOrders[0].price
            lowestPriceID = self.listSellOrders[0].sellerID

            for sellOrder in self.listSellOrders:
                if (sellOrder.price < lowestPrice):
                    lowestPrice = sellOrder.price
                    lowestPriceID = sellOrder.sellerID

            return lowestPrice, lowestPriceID
        else:
            #   Sell order list is empty
            return False, False

    def prepareRound(self):
        #   Prepare the market for consumers
        #   Each seller will price goods based on previous round, restock inventory and submit a sell order

        self.dailyRevenue = 0
        self.dailySales = 0

        for seller in self.listSellers:
            
            seller.reset()
            seller.priceGoods()
            seller.restock()

            newSellOrder = seller.placeSellOrder()
            self.addSellOrder(newSellOrder)

    def printOrders(self):
        for order in self.listSellOrders:
            # print("ID " + str(order.sellerID) + ": " + str(order.quantity) + " units @ $" + "{:.2f}".format(order.price) + " ea.")

            with open("simpleTwoGoods/gnbLog.txt", "a") as logFile:
                logFile.write("ID " + str(order.sellerID) + ": " + str(order.quantity) + " units @ $" + 
                              "{:.2f}".format(order.price) + " ea.\n")

    def buyLowest(self, private=True):
        price, ID = self.findLowest()

        for idx in range(0, len(self.listSellOrders)):
            if (ID == self.listSellOrders[idx].sellerID):
                self.listSellOrders[idx].quantity -= 1

                for seller in self.listSellers:
                    if (ID == seller.ID):
                        seller.makeSale(1, price)
                        break

                if (private):
                    self.registerPurchase(price)

                if (self.listSellOrders[idx].quantity == 0):
                    del self.listSellOrders[idx]

                break

    def registerPurchase(self, price):
        self.dailySales += 1
        self.dailyRevenue += price

    def findDailyAvgPrice(self):
        if (self.dailySales > 0):
            return self.dailyRevenue / self.dailySales
        else:
            avgPrice = 0
            totalQuantity = 0
            for sellOrder in self.listSellOrders:
                totalQuantity += sellOrder.quantity
                avgPrice += (sellOrder.quantity * sellOrder.price)
            avgPrice /= totalQuantity
            return avgPrice
        

    def returnOrders(self):
        for order in self.listSellOrders:
            sellerID = order.sellerID

            for seller in self.listSellers:
                if (seller.ID == sellerID):
                    seller.cancelSellOrder(order.quantity)

        self.listSellOrders = []

    def findAvgSellerProfit(self):
        avgProfit = 0
        for seller in self.listSellers:
            avgProfit += seller.findProfit()
        avgProfit /= len(self.listSellers)
        return avgProfit


class Consumer:
    def __init__(self, ID, initFunds = 0):
        self.ID = ID
        self.funds = initFunds
        self.butter = 0
        self.guns = 0
        self.doneShopping = True

    def setBudget(self, budget):
        self.funds = budget

    def reset(self):
        self.butter = 0
        self.guns = 0
        self.doneShopping = False

    def canAfford(self, price):
        if (price == False):
            return False
        else:
            if (self.funds >= price):
                return True
            else:
                return False
        
    def conditionalBuy(self, market):
        lowestPrice, _ = market.findLowest()

        if (self.canAfford(lowestPrice)):
            self.funds -= lowestPrice

            if (market.type == "butter"):
                self.butter += 1
            elif (market.type == "gun"):
                self.guns += 1

            market.buyLowest()
            return True
        else:
            return False

    def calcUtility(self, butter, guns):
        Ab = 1
        Bb = 1
        Ag = 2
        Bg = 1000

        return (Ab * math.log(Bb * butter + 1) + Ag * math.log(Bg * guns + 1))
        # return (Ab * math.sqrt(Bb * butter) + Ag * math.sqrt(Bg * guns))

    def calcMargUtility(self):
        butterMU = self.calcUtility(self.butter + 1, self.guns) - self.calcUtility(self.butter, self.guns)
        gunsMU = self.calcUtility(self.butter, self.guns + 1) - self.calcUtility(self.butter, self.guns)

        return [butterMU, gunsMU]

    def buyMargin(self, listMarkets):
        #   Buy an item from a market on the margin
        #   Return True if item was bought, otherwise False

        if (not self.doneShopping):
            listMU = self.calcMargUtility()
            listMUP = list(range(NUM_TYPES))
            listPrices = list(range(NUM_TYPES))

            #   Calculate MU-price ratio
            for good in range(NUM_TYPES):
                price, _= listMarkets[good].findLowest()

                if (not (price == False)):
                    listMUP[good] = listMU[good] / price
                    listPrices[good] = price

            if (self.canAfford(listPrices[0])):         #   Can afford butter
                if (self.canAfford(listPrices[1])):     #   Can afford gun
                    # Trade off
                    index_max = np.argmax(listMUP)

                    if (index_max == 0):
                        #   Buy butter
                        return self.conditionalBuy(listMarkets[0])
                    elif (index_max == 1):
                        #   Buy gun
                        return self.conditionalBuy(listMarkets[1])

                else:
                    #   Buy butter
                    return self.conditionalBuy(listMarkets[0])
            else:
                if (self.canAfford(listPrices[1])):
                    #   Buy gun
                    return self.conditionalBuy(listMarkets[1])
                else:
                    #   Can't afford anything
                    self.doneShopping = True
                    return False
        else:
            return False


def generateConsumers(numConsumers = NUM_CONSUMERS):
    listConsumers = []

    for i in range(0, numConsumers):
        listConsumers.append(Consumer(i))

    return listConsumers

def main():
    #   Wipe log file
    with open("simpleTwoGoods/gnbLog.txt", "w") as logFile:
        logFile.write("Butter sellers: " + str(NUM_BUTTER_SELLERS) + "\n")
        logFile.write("Consumers: " + str(NUM_CONSUMERS) + "\n")
        logFile.write("\n")

    butterMarket = Market("butter", NUM_BUTTER_SELLERS)
    gunMarket = Market("gun", NUM_GUN_SELLERS)
    listConsumers = generateConsumers(NUM_CONSUMERS)

    arrAvgButterPrice = np.zeros(SIM_LENGTH)
    arrButterSales = np.zeros(SIM_LENGTH)
    arrAvgGunPrice = np.zeros(SIM_LENGTH)
    arrGunSales = np.zeros(SIM_LENGTH)
    arrAvgUtility = np.zeros(SIM_LENGTH)

    govtGuns = INIT_GOVT_GUNS
    govtButter = INIT_GOVT_BUTTER

    for day in range(SIM_LENGTH):

        if (day < 29):
            govtGuns = INIT_GOVT_GUNS
        elif (day < 69):
            govtGuns = 3 * INIT_GOVT_GUNS
        else:
            govtGuns = INIT_GOVT_GUNS

        # govtGuns = int((1 + 3 * (day/SIM_LENGTH)) * INIT_GOVT_GUNS)
        # govtButter = int((1 + 3 * (day/SIM_LENGTH)) * INIT_GOVT_BUTTER)

        #   Prepare market
        butterMarket.prepareRound()
        gunMarket.prepareRound()

        # print()
        # print("========================= DAY " + str(day + 1) + " =========================")
        # print()
        # print("Initial sell orders")

        with open('simpleTwoGoods/gnbLog.txt', 'a') as logFile:
            logFile.write("========================= DAY " + str(day + 1) + " =========================\n")
            logFile.write("\n")
            logFile.write("Initial butter sell orders\n")

        butterMarket.printOrders()

        with open('simpleTwoGoods/gnbLog.txt', 'a') as logFile:
            logFile.write("\n")
            logFile.write("Initial gun sell orders\n")

        gunMarket.printOrders()
        
        with open('simpleTwoGoods/gnbLog.txt', 'a') as logFile:
            logFile.write("\n")

        #   Government buys guns
        for i in range(govtGuns):
            gunMarket.buyLowest(False)

        #   Govt buys butter
        for i in range(govtButter):
            butterMarket.buyLowest(False)

        #   Consumers receive money
        for consumer in listConsumers:
            consumer.reset()
            consumer.setBudget(DAILY_BUDGET)

        #   Consumers attempt to buy necessities in random order
        randomOrder = list(range(0, NUM_CONSUMERS))
        random.shuffle(randomOrder)

        for randIdx in randomOrder:
            for i in range(BUTTER_SUBSISTENCE):
                listConsumers[randIdx].conditionalBuy(butterMarket)

        # with open('simpleTwoGoods/gnbLog.txt', 'a') as logFile:
        #     logFile.write("After necessities\n")
        # butterMarket.printOrders()
        # with open('simpleTwoGoods/gnbLog.txt', 'a') as logFile:
        #     logFile.write("\n")

        #   Consumers now maximise utility on the margin while any consumer is still shopping
        consumersDone = 0
        listMarkets = [butterMarket, gunMarket]

        while (not (consumersDone == NUM_CONSUMERS)):
            for randIdx in randomOrder:
                if (not listConsumers[randIdx].buyMargin(listMarkets)):
                    consumersDone += 1

            if (consumersDone < len(randomOrder)):
                consumersDone = 0

        with open("simpleTwoGoods/gnbLog.txt", "a") as logFile:
            logFile.write("After utility maximisation\n")
            logFile.write("Butter sell orders\n")
        butterMarket.printOrders()

        with open("simpleTwoGoods/gnbLog.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("Gun sell orders\n")
        gunMarket.printOrders()

        dailyAvgPriceButter = butterMarket.findDailyAvgPrice()
        dailyAvgPriceGun = gunMarket.findDailyAvgPrice()

        with open("simpleTwoGoods/gnbLog.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("Daily butter sales: " + str(butterMarket.dailySales) + "\n")
            logFile.write("Daily average butter price: " + "{:.2f}".format(dailyAvgPriceButter) + "\n")
            logFile.write("\n")
            logFile.write("Daily gun sales: " + str(gunMarket.dailySales) + "\n")
            logFile.write("Daily average gun price: " + "{:.2f}".format(dailyAvgPriceGun) + "\n")
            logFile.write("\n")

        butterMarket.returnOrders()
        gunMarket.returnOrders()

        avgButterProfit = butterMarket.findAvgSellerProfit()
        avgGunProfit = gunMarket.findAvgSellerProfit()

        with open("simpleTwoGoods/gnbLog.txt", "a") as logFile:
            logFile.write("Average butter seller profit: " + "{:.2f}".format(avgButterProfit) + "\n")
            logFile.write("Average gun seller profit: " + "{:.2f}".format(avgGunProfit) + "\n")
            logFile.write("\n")

        avgUtility = 0
        for consumer in listConsumers:
            avgUtility += consumer.calcUtility(consumer.butter, consumer.guns) / NUM_CONSUMERS

        arrDays = list(range(1, SIM_LENGTH + 1))
        arrAvgButterPrice[day] = dailyAvgPriceButter
        arrButterSales[day] = butterMarket.dailySales
        arrAvgGunPrice[day] = dailyAvgPriceGun
        arrGunSales[day] = gunMarket.dailySales
        arrAvgUtility[day] = avgUtility

    plt.figure(1)
    plt.plot(arrDays, arrAvgButterPrice, label="Butter")
    plt.plot(arrDays, arrAvgGunPrice, label="Guns")
    plt.title("Average Market Price")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.legend()

    plt.figure(2)
    plt.plot(arrDays, arrButterSales, label="Butter")
    plt.plot(arrDays, arrGunSales, label="Guns")
    plt.title("Daily Unit Sales")
    plt.xlabel("Time")
    plt.ylabel("Units")
    plt.legend()

    plt.figure(3)
    plt.plot(arrDays, arrAvgUtility, label="Utility")
    plt.title("Average Consumer Utility")
    plt.xlabel("Time")
    plt.ylabel("Utility")

    plt.show()


if (__name__ == "__main__"):
    main()