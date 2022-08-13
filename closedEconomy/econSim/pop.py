from ctypes import util
from .consts import *

class Pop:
    def __init__(self, jobType, initSavings):
        self.jobType = jobType
        self.funds = 0
        self.savings = initSavings
        self.employed = False
        self.studying = 0
        self.income = 0
        self.inv = [0] * NUM_GOOD_TYPES
        self.doneShopping = False

    def reset(self):
        self.employed = False
        self.income = 0
        self.inv = [0] * NUM_GOOD_TYPES

        if (self.studying > 0):
            self.studying -= 1

        self.savings += self.funds
        self.doneShopping = False

    def remunerate(self, wage):
        self.income = wage
        self.employed = True

    def saveMoney(self):
        self.funds = self.income + self.savings
        self.savings = self.funds * SAVINGS_RATE
        self.funds -= self.savings

    def calcUtil(self, listInv):

        if (listInv[TYPE_PRODUCE] > 0):
            hasFood = 1
        else:
            hasFood = 0

        if ((self.jobType == JOB_MAGNATE)):
            foodUtil = math.pow(listInv[TYPE_PRODUCE], 1/8)
            # foodUtil = 10 - (1/10) * pow(listInv[TYPE_PRODUCE] - 10, 2)
            # foodUtil = math.log(listInv[TYPE_ENERGY] + 1)
            energyUtil = 3*math.pow(listInv[TYPE_ENERGY], 1/2)
            utility = hasFood * (foodUtil + energyUtil + 1)
            # utility = energyUtil
        elif ((self.jobType == JOB_ADMINISTRATOR) or (self.jobType == JOB_TECHNOLOGIST)):
            foodUtil = math.pow(listInv[TYPE_PRODUCE], 1/8)
            # foodUtil = 10 - (1/10) * pow(listInv[TYPE_PRODUCE] - 10, 2)
            # foodUtil = math.log(listInv[TYPE_ENERGY] + 1)
            energyUtil = 2*math.pow(listInv[TYPE_ENERGY], 1/2)
            utility = hasFood * (foodUtil + energyUtil + 1)
            # utility = energyUtil
        elif ((self.jobType == JOB_LABOURER) or (self.jobType == JOB_OPERATOR) or (self.jobType == 
        JOB_SOLDIER) or (self.jobType == JOB_CLERK)):
            foodUtil = math.pow(listInv[TYPE_PRODUCE], 1/8)
            # foodUtil = 10 - (1/10) * pow(listInv[TYPE_PRODUCE] - 10, 2)
            # foodUtil = math.log(listInv[TYPE_ENERGY] + 1)
            energyUtil = math.pow(listInv[TYPE_ENERGY], 1/2)
            utility = hasFood * (foodUtil + energyUtil + 1)
            # utility = energyUtil

        return utility

    def calcMargUtil(self):
        listMU = []
        currUtil = self.calcUtil(self.inv)
        for goodType in range(NUM_GOOD_TYPES):
            newInv = self.inv.copy()
            newInv[goodType] += 1
            newUtil = self.calcUtil(newInv)
            margUtil = newUtil - currUtil
            if (margUtil < 0):
                margUtil = 0

            listMU.append(margUtil)

        return listMU

    def maximiseUtility(self, prices: list, available: list):

        if (self.doneShopping):
            return False, None
        else:

            listPrices = prices.copy()
            listAvailable = available.copy()

            #   If good too expensive or no more in stock, make note
            for goodType in range(NUM_GOOD_TYPES):
                if ((listPrices[goodType] > self.funds) or (listAvailable[goodType] < 1)):
                    listPrices[goodType] = -1

            listMU = self.calcMargUtil()
            listMUP = []
            for goodType in range(NUM_GOOD_TYPES):
                listMUP.append(listMU[goodType] / listPrices[goodType])

            maxMUP = max(listMUP)
            maxMUPType = listMUP.index(maxMUP)

            if (maxMUP > 0):
                self.funds -= listPrices[maxMUPType]
                self.inv[maxMUPType] += 1
                return True, maxMUPType
            else:
                self.doneShopping = True
                return False, None