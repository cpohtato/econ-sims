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
                newFirm = Firm(count, goodType, INIT_PRICE[goodType], INIT_WAGES)
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

                    #   For now, transfer all capitalist savings into business
                    self.listFirms[goodType][idx].funds = capitalist.funds
                    capitalist.savings = 0

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
        # 3. Pay capitalists, negotiate labour contracts, pay wages to workers
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
        # 10. Close accounts, calculate stats
        #

        self.stepPops()
        self.stepFirms()
        self.stepEmployment()
        self.stepBenefits()
        self.stepIncomeTax()
        self.stepProduce()
        self.stepPublicProcurement()
        self.stepPrivateProcurement()
        self.stepCompanyTax()
        self.stepClose()
        
        return True

    def stepPops(self):
        #   Pops do not promote yet
        pass

    def stepFirms(self):
        #   Firms do not enter, exit or acquire capital equipment yet
        pass

    def stepEmployment(self):

        self.determineLabourDemand()
        self.supplyLabour()
        self.closeLabourMarkets()

    def stepBenefits(self):
        #   No unemployment subsidies yet
        pass

    def stepIncomeTax(self):
        #   No income tax collected yet
        pass

    def stepProduce(self):
        pass

    def stepPublicProcurement(self):
        #   No public procurement yet
        pass

    def stepPrivateProcurement(self):
        pass

    def stepCompanyTax(self):
        #   No company tax yet
        pass

    def stepClose(self):
        pass

    def determineLabourDemand(self):
        # 1. Firms pay owners dividends
        # 2. Firms determine labour demand and price
        # 3. Place available contracts in labour markets

        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:

                #   Firm pays its owner dividends
                for capitalist in self.listPops[JOB_CAPITALIST]:
                    if (firm.ownerID == capitalist.popID):
                        capitalist.funds += firm.payDividends()
                        break

                #   Firm determines labour demand
                firm.determineLabour()

                #   Firm produces labour orders
                for jobType in range(NUM_JOB_TYPES-1):
                    self.listLabourMarkets[jobType].addOrder(firm.demandLabour(jobType))

    def supplyLabour(self):
        # 1. Workers compare highest wage against reserve price
        # 2. Firms pay workers wages

        listGoodPrices = []
        for goodType in range(NUM_GOOD_TYPES):
            listGoodPrices.append(self.listGoodMarkets[goodType].getPrevAvgPrice())

        for jobType in range(NUM_JOB_TYPES-1):
            highestWage = self.listLabourMarkets[jobType].findHighest()
            randOrder = list(range(len(self.listPops[jobType])))
            random.shuffle(randOrder)

            for idx in randOrder:
                #   If highest wage available is acceptable, then take job
                if (self.listPops[jobType][idx].offerWage(highestWage, listGoodPrices)):
                    self.listPops[jobType][idx].acceptJob(self.listLabourMarkets[jobType]
                    .acceptHighest())
                    highestWage = self.listLabourMarkets[jobType].findHighest()

    def closeLabourMarkets(self):    
        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:
                firmID = firm.firmID

                for jobType in range(NUM_JOB_TYPES-1):
                    firm.receiveLabour(self.listLabourMarkets[jobType].supplyLabour(firmID))

        for jobType in range(NUM_JOB_TYPES-1):
            self.listLabourMarkets[jobType].close()

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
