from .utils import *

class Pop():
    def __init__(self, popID: int, jobType: int, initSavings: float):
        self.popID: int = popID
        self.jobType: int = jobType
        self.funds: float = initSavings
        self.firstName: str = (random.choice(MALE_FIRST_NAMES_DATA)).rstrip()
        self.surname: str = (random.choice(SURNAMES_DATA)).rstrip()
        self.ownFirmID: int = None

        self.reserveWageGoods: list[float] = []
        for goodType in range(NUM_GOOD_TYPES):
            minGood = random.gauss(RESERVE_WAGE_MEAN[self.jobType][goodType],
            RESERVE_WAGE_NORM_STD_DEV[jobType][goodType] * RESERVE_WAGE_NORM_STD_DEV[jobType]
            [goodType])

            if (minGood < RESERVE_WAGE_MIN[jobType][goodType]):
                minGood = RESERVE_WAGE_MIN[jobType][goodType]

            self.reserveWageGoods.append(minGood)

        self.employed: bool = False
        self.prevIncome: float = 0
        self.currIncome: float = 0.0
        self.doneShopping = False

        #   Randomly generate consumption preferences
        self.goodPref = []
        for goodType in range(NUM_GOOD_TYPES):
            coefficient = random.gauss(GOOD_PREF_MEAN[goodType], 
            GOOD_PREF_NORM_STD_DEV[goodType] * GOOD_PREF_MEAN[goodType])
            if (coefficient < 0):
                coefficient = 0
            self.goodPref.append(coefficient)

        self.inv = [0 for i in range(NUM_GOOD_TYPES)]

        self.utils = 0

    def getFullName(self):
        fullName: str = self.firstName + " " + self.surname
        return fullName

    def offerWage(self, highestWage: float, listGoodPrices: list[float]):
        reserveWage = 0

        for goodType in range(NUM_GOOD_TYPES):
            reserveWage += listGoodPrices[goodType] * self.reserveWageGoods[goodType]

        if (highestWage >= reserveWage):
            #   Return true if highest wage available is acceptable
            return True
        else:
            #   Otherwise decline job
            return False

    def acceptJob(self, wage: float):
        self.employed = True
        self.currIncome = wage
        self.funds += wage

    def acceptDividends(self, dividends: float):
        self.currIncome = dividends
        self.funds += dividends

    def calcUtil(self, basket: list[int]):
        if (basket[TYPE_FOOD] > 0):
            hasFood = 1
        else:
            hasFood = 0

        utility: float = 0
        for goodType in range(NUM_GOOD_TYPES):
            utility += self.goodPref[goodType] * math.sqrt(basket[goodType])

        utility *= hasFood

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

    def maximiseUtility(self, prices: list[float]):

        if (self.doneShopping):
            return False, None
        else:

            listPrices = prices.copy()

            #   If good too expensive or no more in stock, make note
            for goodType in range(NUM_GOOD_TYPES):
                if ((listPrices[goodType] > self.funds)):
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

    def consumeGoods(self):
        self.utils = self.calcUtil(self.inv)
        self.inv = [0 for i in range(NUM_GOOD_TYPES)]

    def reset(self):
        self.employed: bool = False
        self.prevIncome: float = self.currIncome
        self.currIncome: float = 0.0
        self.doneShopping = False

    def log(self):
        with open("simpleClosedEconomy/log/pops.txt", "a") as logFile:
            logFile.write(self.firstName + " " + self.surname + ", " + DICT_JOB_TITLES[self.
            jobType] + ": " + "{:.2f}".format(self.utils) + " utils\n")