from tokenize import Double
from econ_funcs import *

class SellOrder:
    def __init__(self, goodType, firmID, quantity: int, price: Double):
        self.goodType = goodType
        self.firmID = firmID
        self.quantity = quantity
        self.price = price

class LabourOrder:
    def __init__(self, jobType, firmGoodType, firmID, quantity: int, wage: Double):
        self.jobType = jobType
        self.firmGoodType = firmGoodType
        self.firmID = firmID
        self.quantity = quantity
        self.wage = wage
 
class Demo:
    #   Stands for 1000 people
    def __init__(self, jobType, initFunds, initMorale):
        self.jobType = jobType
        self.funds = initFunds
        self.morale = initMorale
        self.employed = False
        self.employerID = None
        self.employerType = None
        self.inv = [0] * NUM_GOOD_TYPES

    def canAfford(self, price):
        if (self.funds > price):
            return True
        else:
            return False

    def reset(self):
        self.employed = False
        self.employerID = None
        self.employerType = None
        self.inv = [0] * NUM_GOOD_TYPES

    def pickContract(self, labourMarket):
        wage, firmID, firmType = labourMarket.findHighest()

        if (not (firmID == None)):
            if (wage > INIT_WAGES[self.jobType]/2):
                self.employed = True
                self.funds += wage
                self.employerID = firmID
                self.employerType = firmType
                labourMarket.acceptHighest()

    def findUtility(self, listGoods):
        utility = math.log(listGoods[TYPE_PRODUCE] + 1) + math.log(listGoods[TYPE_ENERGY] + 1) 
        + 3 * math.log(listGoods[TYPE_PROCESSED_FOOD] + 1)
        return utility

    def findMargUtility(self):
        listMU = [0] * NUM_GOOD_TYPES

        for goodType in range(NUM_GOOD_TYPES):
            marginalInv = self.inv.copy()
            marginalInv[goodType] += 1
            listMU[goodType] = self.findUtility(marginalInv) - self.findUtility(self.inv)

        return listMU

    def buyMargin(self, listGoodMarkets):
        listMU = self.findMargUtility()
        listGoodTypes = list(range(NUM_GOOD_TYPES))

        listValidMUP = []
        listValidGoodTypes = []

        listPrices = []
        for market in listGoodMarkets:
            price, _ = market.findLowest()
            listPrices.append(price)
        
        listMUP = []
        for goodType in range(NUM_GOOD_TYPES):
            if (listPrices[goodType] == None):
                listMUP.append(None)
            else:
                if (listPrices[goodType] == 0):
                    listMUP.append(0)
                else:
                    listMUP.append(listMU[goodType] / listPrices[goodType])

        for idx in range(len(listGoodTypes)):
            if ((listMUP[idx] == None) or (listMUP[idx] == 0)):
                pass
            else:
                listValidMUP.append(listMUP[idx])
                listValidGoodTypes.append(listGoodTypes[idx])

        listMUP = listValidMUP
        listGoodTypes = listValidGoodTypes

        chosen = False
        bought = False
        while not chosen:
            if (listMUP):
                maxMUP = max(listMUP)
                maxIdx = listMUP.index(maxMUP)
                maxGoodType = listGoodTypes[maxIdx]

                price, _ = listGoodMarkets[maxGoodType].findLowest()
                if (self.canAfford(price)):
                    #   Buy
                    self.funds -= price
                    self.inv[maxGoodType] += 1
                    listGoodMarkets[maxGoodType].buyLowest()
                    chosen = True
                    bought = True
                else:
                    del listMUP[maxIdx]
                    del listGoodTypes[maxIdx]
            else:
                #   Nothing to buy
                chosen = True
                bought = False

        return bought        


class Firm:
    def __init__(self, goodType, firmID, size, initFunds, initLabourDemands, initWages, initEmployees, prevPrice):
        self.goodType = goodType
        self.firmID = firmID
        self.size = size
        self.funds = initFunds
        self.listBaseLabourDemands = findBaseLabourDemands(self.goodType)
        self.listPrevLabourDemands = initLabourDemands
        self.listPrevWages = initWages
        self.listPrevEmployees = initEmployees
        self.listCurrLabourDemands = [0] * NUM_JOB_TYPES
        self.listCurrWages = [0] * NUM_JOB_TYPES
        self.listCurrEmployees = [0] * NUM_JOB_TYPES

        #   Initialise inventory and start with a free 300 points of production
        self.listInv: list[int] = [0] * NUM_GOOD_TYPES
        self.listTargetInv: list[int] = [0] * NUM_GOOD_TYPES
        self.listInv[self.goodType] = int(300 / GOOD_COST[self.goodType])
        self.listTargetInv[self.goodType] = int(300 / GOOD_COST[self.goodType])

        self.currExpenditure = 0
        self.price = prevPrice
        self.prevSales = int(50.0 / GOOD_COST[self.goodType])
        self.currSales = 0
        self.currRevenue = 0
        self.currExpenditure = 0

    def determineLabour(self, listAvgWages, listProductivity):

        #   Scale labour demand to firm size and determine wage offer
        for job in range(NUM_JOB_TYPES):
            if (self.listBaseLabourDemands[job] > 0):
                self.listCurrLabourDemands[job] = self.listBaseLabourDemands[job] * self.size 

                labourShortage = (self.listPrevLabourDemands[job] - self.listPrevEmployees[job])

                # if (labourShortage / self.listPrevLabourDemands[job] > 0):
                #     self.listCurrWages[job] = self.listPrevWages[job] 
                #     + random.uniform(0, WAGE_VISCOSITY) * listProductivity[job] * (labourShortage 
                #     / self.listPrevLabourDemands[job])
                # else:
                #     self.listCurrWages[job] = random.uniform(1 - WAGE_VISCOSITY, 1) * self.listPrevWages[job]
                #     + 0.5 * WAGE_VISCOSITY * (listAvgWages[job] - self.listPrevWages[job])

                if (labourShortage / self.listPrevLabourDemands[job] > 0):
                    self.listCurrWages[job] = self.listPrevWages[job] * random.uniform(1, 1 + WAGE_VISCOSITY)

                else:
                    self.listCurrWages[job] = self.listPrevWages[job] * random.uniform(1 - WAGE_VISCOSITY, 1)


                self.listCurrWages[job] = round(self.listCurrWages[job], 2)

            else:
                self.listCurrWages[job] = 0

    def produceLabourOrders(self):
        """
        Returns list of labour orders to be sorted into appropriate labour markets
        """

        listLabourOrder = []

        for job in range(NUM_JOB_TYPES):
            if (self.listCurrLabourDemands[job] > 0):
                order = LabourOrder(job, self.goodType, self.firmID, self.listCurrLabourDemands[job], self.listCurrWages[job])
                listLabourOrder.append(order)
                self.funds -= self.listCurrLabourDemands[job] * self.listCurrWages[job]

                self.listCurrEmployees[job] = self.listCurrLabourDemands[job]

        return listLabourOrder

    def produceGoods(self, listProductivity, listMarkets):
        """
        Place sell order in appropriate market after producing and pricing goods
        """

        #   Calculate accumulated production points
        #   Can be more complicated in the future but just a sum of linear terms for now
        productionPoints = 0
        for jobType in range(NUM_JOB_TYPES):
            productionPoints += self.listCurrEmployees[jobType] * listProductivity[jobType]

        #   Produce goods
        #   Commodity industries don't require external resource inputs
        if ((self.goodType == TYPE_ORE) or (self.goodType == TYPE_RARE_EARTHS) or 
            (self.goodType == TYPE_PRODUCE) or (self.goodType == TYPE_ENERGY) or
            (self.goodType == TYPE_VOLATILES)):

            unitsProduced = int(productionPoints) / GOOD_COST[self.goodType]

        elif (self.goodType == TYPE_ELECTRONICS):
            pass
        elif (self.goodType == TYPE_QUANTRONICS):
            pass
        elif (self.goodType == TYPE_ALLOYS):
            pass
        elif (self.goodType == TYPE_COMPOSITES):
            pass
        elif (self.goodType == TYPE_MACHINERY):
            pass
        elif (self.goodType == TYPE_SPECIALISED_MACHINERY):
            pass
        elif (self.goodType == TYPE_AUTOMATONS):
            pass
        elif (self.goodType == TYPE_LIGHT_TRANSPORT):
            pass
        elif (self.goodType == TYPE_LIGHT_ORDNANCE):
            pass
        elif (self.goodType == TYPE_HEAVY_TRANSPORT):
            pass
        elif (self.goodType == TYPE_HEAVY_ORDNANCE):
            pass
        elif (self.goodType == TYPE_SERVICES):
            pass
        elif (self.goodType == TYPE_PROCESSED_FOOD):
            pass
        elif (self.goodType == TYPE_CONSUMER_GOODS):
            pass
        elif (self.goodType == TYPE_LUXURY_GOODS):
            pass

        #   Add labour costs
        for jobType in range(NUM_JOB_TYPES):
            self.currExpenditure += self.listCurrEmployees[jobType] * self.listCurrWages[jobType]
        
        #   Price floor
        if (self.currExpenditure > 0):
            self.costPerUnit = unitsProduced / self.currExpenditure

        # Pricing logic
        surplus = self.listInv[self.goodType] - self.listTargetInv[self.goodType]

        # if (unitsProduced > self.prevSales):
        #     self.price = random.uniform(1 - PRICE_VISCOSITY, 1) * (1 - 
        #     SURPLUS_CONST * (surplus/self.listTargetInv[self.goodType])) * self.price
        # else:
        #     self.price = random.uniform(1, 1 + PRICE_VISCOSITY) * (1 - 
        #     SURPLUS_CONST * (surplus/self.listTargetInv[self.goodType])) * self.price

        if (surplus > 0):
            self.price *= random.uniform(1 - PRICE_VISCOSITY, 1)
        else:
            self.price *= random.uniform(1, 1 + PRICE_VISCOSITY)

        if (self.price < self.costPerUnit):
            self.price = self.costPerUnit

        self.price = round(self.price, 2)

        self.listInv[self.goodType] += unitsProduced

        sellOrder = self.produceSellOrder()

        listMarkets[self.goodType].addSellOrder(sellOrder)

    def produceSellOrder(self):
        sellOrder = SellOrder(self.goodType, self.firmID, self.listInv[self.goodType], self.price)
        self.currRevenue = self.listInv[self.goodType] * self.price
        self.listInv[self.goodType] = 0
        
        return sellOrder

    def reset(self):
        self.listPrevEmployees = self.listCurrEmployees
        self.listPrevLabourDemands = self.listCurrLabourDemands
        self.listPrevWages = self.listCurrWages

        self.listCurrEmployees = [0] * NUM_JOB_TYPES

        self.currExpenditure = 0
        self.prevSales = self.currSales
        self.currSales = 0
        self.currRevenue = 0


class LabourMarket:
    def __init__(self, jobType, initContractsAccepted, initWagesPaid):
        self.jobType = jobType
        self.contractsAccepted = initContractsAccepted
        self.totalWagesPaid = initWagesPaid
        self.listLabourOrders: list[LabourOrder] = []

    def resetStats(self):
        self.totalWagesPaid = 0
        self.contractsAccepted = 0

    def findAvgWageAccepted(self):
        if (self.contractsAccepted > 0):
            return self.totalWagesPaid / self.contractsAccepted
        else:
            return 0.00

    def findAvgWageOffered(self):
        avgWage = 0
        vacancies = 0

        #   Duplicate code because efficiency
        for order in self.listLabourOrders:
            avgWage += order.wage * order.quantity
            vacancies += order.quantity

        if (vacancies > 0):
            avgWage = avgWage / vacancies

        return avgWage

    def findTotalVacancies(self):
        vacancies = 0

        for order in self.listLabourOrders:
            vacancies += order.quantity

        return vacancies

    def findHighest(self):
        highestWage = 0
        highestWageID = None
        highestWageType = None

        for order in self.listLabourOrders:
            if (order.wage > highestWage):
                highestWage = order.wage
                highestWageID = order.firmID
                highestWageType = order.firmGoodType

        return highestWage, highestWageID, highestWageType

    def acceptHighest(self):
        wage, firmID, firmType = self.findHighest()

        for idx in range(0, len(self.listLabourOrders)):
            if ((firmID == self.listLabourOrders[idx].firmID) and (firmType == self.listLabourOrders[idx].firmGoodType)):
                self.listLabourOrders[idx].quantity -= 1

                if (self.listLabourOrders[idx].quantity == 0):
                    del self.listLabourOrders[idx]

                break

        self.registerAcceptance(wage)

    def registerAcceptance(self, wage):
        self.totalWagesPaid += wage
        self.contractsAccepted += 1

    def addLabourOrder(self, order: LabourOrder):
        if (order.jobType == self.jobType):
            self.listLabourOrders.append(order)
        else:
            print("Tried to add " + str(DICT_JOB_TITLES[order.jobType]) + " to " 
            + str(DICT_JOB_TITLES[self.jobType]) + " job market")

    def close(self, listFirms: list[list[Firm]]):
        for order in self.listLabourOrders:
            for goodType in range(NUM_GOOD_TYPES):
                for firm in listFirms[goodType]:
                    if ((order.firmGoodType == firm.goodType) and (order.firmID == firm.firmID)):
                        firm.listCurrEmployees[order.jobType] -= order.quantity
                        firm.funds += order.wage * order.quantity

        self.listLabourOrders = []

    def log(self):
        accepted = self.contractsAccepted
        vacancies = accepted + self.findTotalVacancies()
        avgAcceptedWage = self.findAvgWageAccepted()

        with open("closedEconomy/log/labourOrders.txt", "a") as logFile:
            # logFile.write(DICT_JOB_TITLES[self.jobType] + " Job Market" + "\n")

            # for order in self.listLabourOrders:
            #     logFile.write(str(order.firmGoodType) + "-" + str(order.firmID) + ": " + str(order.quantity) 
            #     + " @ $" + "{:.2f}".format(order.wage) + "\n")
            
            # logFile.write("\n")
            # logFile.write("Total vacancies: " + str(self.findTotalVacancies()) + "\n")
            logFile.write(DICT_JOB_TITLES[self.jobType] + " Jobs: " + str(accepted) + "/" + str(vacancies) + " accepted\n")
            logFile.write("Average wage accepted: $" + "{:.2f}".format(avgAcceptedWage) + "\n")
            # logFile.write("Average wage offered: $" + "{:.2f}".format(self.findAvgWageOffered()) + "\n")
            # logFile.write("\n")
            logFile.write("\n")



class GoodMarket:
    def __init__(self, goodType):
        self.goodType = goodType
        self.listSellOrders: list[SellOrder] = []

        self.totalRevenue = 0
        self.totalSales = 0

        self.avgPrice = 0
        self.totalOffered = 0

    def reset(self):
        self.totalRevenue = 0
        self.totalSales = 0

    def addSellOrder(self, order: SellOrder):
        if (order.goodType == self.goodType):
            self.listSellOrders.append(order)
        else:
            print("Tried to add " + str(DICT_GOOD_NAMES[order.goodType]) + " to " 
            + str(DICT_GOOD_NAMES[self.goodType]) + " market")

    def findLowest(self):
        if (self.listSellOrders):
            lowestPrice = self.listSellOrders[0].price
            lowestPriceID = self.listSellOrders[0].firmID

            for sellOrder in self.listSellOrders:
                if (sellOrder.price < lowestPrice):
                    lowestPrice = sellOrder.price
                    lowestPriceID = sellOrder.firmID

            return lowestPrice, lowestPriceID
        else:
            return False, False

    def buyLowest(self):
        price, firmID = self.findLowest()

        if not (price == False):
            for idx in range(len(self.listSellOrders)):
                if (firmID == self.listSellOrders[idx].firmID):
                    self.listSellOrders[idx].quantity -= 1
                    self.registerSale(price)

                    if (self.listSellOrders[idx].quantity == 0):
                        del self.listSellOrders[idx]

                    break

    def registerSale(self, price):
        self.totalRevenue += price
        self.totalSales += 1

    def calcStats(self):
        if (self.totalSales > 0):
            self.avgPrice = self.totalRevenue/self.totalSales
        else:
            self.avgPrice = 0

        self.totalOffered = self.totalSales
        for order in self.listSellOrders:
            self.totalOffered += order.quantity


    def close(self, listFirms: list[list[Firm]]):
        self.calcStats()

        for order in self.listSellOrders:
            for firm in listFirms[self.goodType]:
                if (order.firmID == firm.firmID):
                    firm.listInv[order.goodType] += order.quantity
                    firm.currRevenue -= order.quantity * order.price
        
        self.listSellOrders = []

        self.log()

    def log(self):
        with open("closedEconomy/log/sellOrders.txt", "a") as logFile:
            logFile.write(DICT_GOOD_NAMES[self.goodType] + " Market:\n")
            logFile.write("Sales: " + str(self.totalSales) + "/" + "{:.0f}".format(self.totalOffered) + "\n")
            logFile.write("Avg. price: " + "{:.2f}".format(self.avgPrice) + "\n")
            
            # for order in self.listSellOrders:
            #     logFile.write("ID " + str(order.firmID) + ": " + "{:.0f}".format(order.quantity) + 
            #     " units @ $" + "{:.2f}".format(order.price) + " ea.\n")

            logFile.write("\n")

class Govt:
    def __init__(self):
        pass
    

def generateInitDemos():
    initDemos = []

    for i in range(NUM_JOB_TYPES):
        num = INIT_POPULATION[i]
        for j in range(num):
            initDemos.append(Demo(i, INIT_WAGES[i], 1))

    return initDemos


def generateInitFirms():
    initFirms = [[] for i in range(NUM_GOOD_TYPES)]

    for goodType in range(NUM_GOOD_TYPES):
        num = INIT_FIRMS[goodType]
        for j in range(num):
            prevLabour = findBaseLabourDemands(goodType)
            initFirms[goodType].append(Firm(goodType, j, 1, 1000, prevLabour, 
            INIT_WAGES, prevLabour, INIT_PRICE[goodType]))

    return initFirms