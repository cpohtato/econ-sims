from .utils import *

class Firm():
    def __init__(self, firmID: int, goodType: int, initPrice: float, initWages: list[float]):
        self.firmID: int = firmID
        self.goodType: int = goodType
        self.ownerID: int = None
        self.name: str = None
        self.funds: float = 0.0

        # Previous step stats, should be updated at the end of every month
        self.prevPrice: float = initPrice
        self.prevListWages: list[float] = initWages
        self.prevListLabourDemand: list[int] = [1, 0]
        self.prevListLabourReceived: list[int] = [1, 0]

        # Current step stats, should be reset at the end of every month
        self.currDividends: float = 0.0
        self.currListWages: list[float] = []

    def generateName(self, surname: str):
        if (self.goodType == TYPE_FOOD):
            companyName: str = random.choice(FOOD_COMPANY_NAME_DATA)
        elif (self.goodType == TYPE_ENERGY):
            companyName: str = random.choice(ENERGY_COMPANY_NAME_DATA)

        self.name = surname + " " + companyName

    def payDividends(self):
        self.currDividends = self.funds * DIVIDEND_RATE
        self.funds -= self.currDividends
        return self.currDividends

    def determineLabour(self):
        #   To hire, firm must make profit; condition given below:
        #   (output price) > (input cost) + (production points) * ((wage) / (marginal productivity))
        #   Where MP is marginal productivity and PP is production point cost, condition is:
        #   (MP / wage) > (PP / ((output price) - (input cost)))
        #   (MP / wage) is the MP-wage ratio (MPW)

        #   First, price labour competitively
        self.currListWages = self.prevListWages.copy()
        for jobType in range(NUM_JOB_TYPES-1):
            demanded = self.prevListLabourDemand[jobType]
            received = self.prevListLabourReceived[jobType]
            if (demanded == received):
                #   Firms will try to squeeze workers on wages if full employment
                self.currListWages[jobType] *= random.uniform(1 - WAGE_VISCOSITY, 1)
                self.currListWages[jobType] = round(self.currListWages[jobType], 2)
            else:
                #   Firms will raise wages to get more workers
                #   Larger labour shortfall will make firm raise wages higher
                shortfall: float = 1 - (float(received)/float(demanded))
                self.currListWages[jobType] *= random.uniform(1, 1 + WAGE_VISCOSITY*(1+shortfall))
                self.currListWages[jobType] = round(self.currListWages[jobType], 2)

        #   Now determine labour demand
        fundsAvailable = (self.funds + self.currDividends) * (1 - FIRM_SAVINGS_RATE)
        fundsAvailable -= self.currDividends
        done = False

        self.currListLabourDemand = [0 for i in range(NUM_JOB_TYPES-1)]

        while not done:
            #   Calculate Marginal Productivity-Wage ratio (MPW ratio)
            listMPW = []
            listMP = self.calcMargProd(self.currListLabourDemand)
            for jobType in range(NUM_JOB_TYPES-1):
                if (fundsAvailable >= self.currListWages[jobType]):
                    listMPW.append(listMP[jobType] / self.currListWages[jobType])
                else:
                    listMPW.append(0)

