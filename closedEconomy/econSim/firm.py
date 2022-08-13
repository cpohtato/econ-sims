from .pop import *

class Firm:
    def __init__(self, goodType, initSize=1, initFunds=None, initMachinery=INIT_MACHINERY,
    initSpecMachinery=INIT_SPEC_MACHINERY):
        self.goodType = goodType
        self.size = initSize

        if (initFunds == None):
            self.funds = TARGET_FUNDS
        else:
            self.funds = initFunds

        self.unitProdPoints = GOOD_COST[goodType]

        self.listEmployees = [0] * NUM_JOB_TYPES

        self.listInv = [0] * NUM_GOOD_TYPES
        self.listInv[TYPE_MACHINERY] = initMachinery
        self.listInv[TYPE_SPECIALISED_MACHINERY] = initSpecMachinery

        self.currExp = 0
        self.currProduced = 0
        self.currSales = 0
        self.currRevenue = 0

        self.prevProfit = 0

    def reset(self):
        self.prevProfit = self.currRevenue - self.currExp
        self.listEmployees = [0] * NUM_JOB_TYPES
        self.currExp = 0
        self.currProduced = 0
        self.currSales = 0
        self.currRevenue = 0
        self.listInv[self.goodType] = 0

    def prodFunc(self, listLabour, listK):
        #   K = capital
        #   Productivity changes of firm size not implemented yet
        #   Should implement function to find base labour demands

        #   CE = Capital Equipment, SCE = Specialised Capital Equipment
        #   Capital-labour ratio scaling factors
        CE = listK[TYPE_MACHINERY] * WORKERS_PER_MACHINE
        SCE = listK[TYPE_SPECIALISED_MACHINERY] * WORKERS_PER_SPEC_MACHINE

        #   Commodity firms
        if ((self.goodType == TYPE_ORE) or (self.goodType == TYPE_RARE_EARTHS) or (self.goodType
         == TYPE_PRODUCE) or (self.goodType == TYPE_ENERGY) or (self.goodType == TYPE_VOLATILES)):
        
            if (listLabour[JOB_MAGNATE] > 0):
                hasMagnate = 1
            else:
                hasMagnate = 0.8

            magnateProd = INIT_PRODUCTIVITY[JOB_MAGNATE] * listLabour[JOB_MAGNATE]**(1/64)
            adminProd =   INIT_PRODUCTIVITY[JOB_ADMINISTRATOR] * (listLabour[
                JOB_ADMINISTRATOR] / 5)**(1/4)

            if (SCE == 0):
                techProd = 0
            else:
                techProd =    (SCE) - (1/SCE) * (listLabour[JOB_TECHNOLOGIST] - SCE)**2

            if (CE == 0):
                labourProd = 0
            else:
                labourProd =  (CE) - (1/CE) * (listLabour[JOB_LABOURER] - CE)**2

            productivity = hasMagnate * (magnateProd + adminProd + 1) * (techProd + labourProd + 1)

            numEmps = 0
            for numType in listLabour:
                numEmps += numType

            if (numEmps < 1):
                productivity = 0

            return productivity
        else:
            raise Exception("Non-commodity firm productivity not implemented yet")

    def getProd(self):
        return self.prodFunc(self.listEmployees, self.listInv)

    def calcMargProd(self):
        listMP = []
        currProd = self.prodFunc(self.listEmployees, self.listInv)

        for jobType in range(NUM_JOB_TYPES):
            newEmp = self.listEmployees.copy()
            newEmp[jobType] += 1
            newProd = self.prodFunc(newEmp, self.listInv)

            margProd = newProd - currProd
            if (margProd < 0):
                margProd = 0

            listMP.append(margProd)

        return listMP

    def calcInputCosts(self, listPrices):

        #   Commodity firms have no input costs
        if ((self.goodType == TYPE_ORE) or (self.goodType == TYPE_RARE_EARTHS) or (self.goodType
         == TYPE_PRODUCE) or (self.goodType == TYPE_ENERGY) or (self.goodType == TYPE_VOLATILES)):
            return 0
        else:
            raise Exception("Non-commodity firm input cost not implemented yet")

    def demandLabour(self, listWages, listAvailable: list, listPrices):
        #   To hire, firm must make profit; condition given below:
        #   (output price) > (input cost) + (production points) * ((wage) / (marginal productivity))
        #   Where MP is marginal productivity and PP is production point cost, condition is:
        #   (MP / wage) > (PP / ((output price) - (input cost)))
        #   (MP / wage) is the MP-wage ratio (MPW)
        #   If labour unavailable, -1 will make MPW a negative number

        #   Rule out labour that is too expensive to hire
        #   Need to reserve money for input costs before this
        #   To be implemented at some later stage
        labourAvailable = listAvailable.copy()
        for jobType in range(NUM_JOB_TYPES):
            if (listWages[jobType] > self.funds):
                labourAvailable[jobType] = -1

        listMPW = []
        listMP = self.calcMargProd()
        for idx in range(NUM_JOB_TYPES):
            listMPW.append(labourAvailable[idx] * listMP[idx] / listWages[idx])

        outputPrice = listPrices[self.goodType]
        inputCosts = self.calcInputCosts(listPrices)
        condition = self.unitProdPoints / (outputPrice - inputCosts)

        maxMPW = max(listMPW)
        maxIdx = listMPW.index(maxMPW)

        if (maxMPW > condition):
            self.funds -= listWages[maxIdx]
            self.currExp += listWages[maxIdx]
            self.listEmployees[maxIdx] += 1
            return True, maxIdx
        else:
            return False, None

    def produceGoods(self, prices: list, available: list):

        listPrices = prices.copy() 
        listAvailable = available.copy()

         #   Commodity firms have no input costs
        if ((self.goodType == TYPE_ORE) or (self.goodType == TYPE_RARE_EARTHS) or (self.goodType
         == TYPE_PRODUCE) or (self.goodType == TYPE_ENERGY) or (self.goodType == TYPE_VOLATILES)):

            qtyProduced = int(self.getProd() / self.unitProdPoints)
            self.listInv[self.goodType] += qtyProduced
            qtyTotal = self.listInv[self.goodType]
            self.currProduced = qtyProduced
            return qtyProduced, qtyTotal

        else:
            raise Exception("Non-commodity firm production not implemented yet")

    def getCurrExp(self):
        return self.currExp

    def getProduced(self):
        return self.currProduced

    def getAvailable(self):
        return self.listInv[self.goodType]

    def getSales(self):
        return self.currSales

    def getProfit(self):
        return self.currRevenue - self.currExp

    def makeSale(self, qty, price):
        self.currSales += qty
        self.listInv[self.goodType] -= qty
        self.funds += qty * price
        self.currRevenue += qty * price

    def payDividends(self):
        if (self.funds > TARGET_FUNDS):
            dividends = self.funds - TARGET_FUNDS
            self.funds = TARGET_FUNDS
            return dividends
        else:
            return 0


    def log(self):
        with open("closedEconomy/log/firms.txt", "a") as logFile:
            logFile.write(DICT_GOOD_NAMES[self.goodType] + ": " + str(self.getSales()) + "/" + 
            str(self.getProduced()) + ", Profit: " + "{:.2f}".format(self.getProfit()) + "\n")

        

        