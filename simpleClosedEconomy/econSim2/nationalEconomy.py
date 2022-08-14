from .labourMarket import *
from .goodMarket import *

class NationalEconomy():
    def __init__(self):
        self.listPops: list[list[Pop]] = self.generateInitPops()
        self.listFirms: list[list[Firm]] = self.generateInitFirms()
        self.assignInitFirms()
        self.listLabourMarkets: list[LabourMarket] = self.generateInitLabourMarkets()
        self.listGoodMarkets: list[GoodMarket] = self.generateInitGoodMarkets()

    def generateInitPops(self):
        listPops = [[] for i in range(NUM_JOB_TYPES)]

        count = 0

        for jobType in range(NUM_JOB_TYPES):
            for pop in range(INIT_POPULATION[jobType]):
                newPop = Pop(count, jobType, INIT_SAVINGS[jobType])
                # print(newPop.getFullName() + ", " + DICT_JOB_TITLES[newPop.jobType])
                listPops[jobType].append(newPop)
                count += 1

        return listPops

    def generateInitFirms(self):
        listFirms = [[] for i in range(NUM_GOOD_TYPES)]

        count = 0

        for goodType in range(NUM_GOOD_TYPES):
            for firm in range(INIT_FIRMS[goodType]):
                newFirm = Firm(count, goodType)
                listFirms[goodType].append(newFirm)
                count += 1

        return listFirms

    def assignInitFirms(self):
        freeCapitalists = len(self.listPops[JOB_CAPITALIST])
        freeFirms = sum(len(self.listFirms[goodType]) for goodType in range(NUM_GOOD_TYPES))

        if (freeCapitalists > freeFirms):
            #   Make free capitalists start their own firms
            print("ERROR: Too many free capitalists")
            return 0
        elif (freeCapitalists < freeFirms):
            #   Make some firms fold?
            print("ERROR: Not enough free capitalists")
            return 0

        for capitalist in self.listPops[JOB_CAPITALIST]:
            goodType = 0
            idx = 0
            while (capitalist.ownFirmID == None):
                if (self.listFirms[goodType][idx].ownerID == None):
                    capitalist.ownFirmID = self.listFirms[goodType][idx].firmID
                    self.listFirms[goodType][idx].ownerID = capitalist.popID
                    self.listFirms[goodType][idx].generateName(capitalist.surname)
                    # print(self.listFirms[goodType][idx].name)
                else:
                    idx += 1

                    if (len(self.listFirms[goodType]) == idx):
                        idx = 0
                        goodType += 1

    def generateInitLabourMarkets(self):
        listLabourMarkets = []

        for jobType in range(NUM_JOB_TYPES):
            if (jobType != JOB_CAPITALIST):
                listLabourMarkets.append(LabourMarket(jobType))

        return listLabourMarkets

    def generateInitGoodMarkets(self):
        listGoodMarkets = []

        for goodType in range(NUM_GOOD_TYPES):
            listGoodMarkets.append(GoodMarket(goodType))

    def monthStep(self, month: int):
        #
        # Step through complete cycle for one time step (month)
        #
        # 1. Determine population promotion, growth/decline
        #
        # 2. Determine firms entering, exiting, growing/shrinking
        #
        # 3. Negotiate labour contracts, pay wages
        #
        # 4. Govt pays unemployment subsidies
        #
        # 5. Govt collects income tax
        #
        # 6. Goods are produced and placed in market stalls
        #
        # 7. Govt buys goods
        #
        # 8. Population buys goods
        #
        # 9. Govt collects company tax
        #
        # 10. Calculate monthly income for capitalists
        
        return True

    def monthlyPrices(self):
        listPrices = []

        for market in range(NUM_GOOD_TYPES):
            listPrices.append(random.randint(1,10))

        return listPrices

    def monthlySales(self):
        listSales = []

        for market in range(NUM_GOOD_TYPES):
            listSales.append(random.randint(1,10))

        return listSales

    def monthlyWages(self):
        listWages = []

        for market in range(NUM_JOB_TYPES):
            listWages.append(random.randint(1,10))

        return listWages

    def monthlyJobs(self):
        listHired = []

        for market in range(NUM_JOB_TYPES):
            listHired.append(random.randint(1,10))

        return listHired
