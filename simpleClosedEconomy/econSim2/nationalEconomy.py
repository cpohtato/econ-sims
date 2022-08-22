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
                    capitalist.funds = 0

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
            listGoodMarkets.append(GoodMarket(goodType, INIT_PRICE[goodType])) 

        return listGoodMarkets

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
        # 10. Firms collect money from market stalls
        #
        # 11. Close accounts, calculate stats
        #

        self.logHeader(month)

        self.stepPops()
        self.stepFirms()
        self.stepEmployment()
        self.stepBenefits()
        self.stepIncomeTax()
        self.stepProduce()
        self.stepPublicProcurement()
        self.stepPrivateProcurement()
        self.stepCloseMarkets()
        self.stepCompanyTax()
        self.stepReset()
        
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
        self.settleLabour()

    def stepBenefits(self):
        #   No unemployment subsidies yet
        pass

    def stepIncomeTax(self):
        #   No income tax collected yet
        pass

    def stepProduce(self):
        #   Firms by good type order produce goods and place them in market stalls for sale 
        
        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:
                firm.acquireRawMaterials()
                goodQty, goodPrice = firm.produceGoods()
                self.listGoodMarkets[goodType].placeGoods(firm.firmID, goodQty, goodPrice)

    def stepPublicProcurement(self):
        #   No public procurement yet
        pass

    def stepPrivateProcurement(self):
        #   Consoom

        #   Find total number of pops and randomise order
        numPops = 0
        for jobType in range(NUM_JOB_TYPES):
            numPops += len(self.listPops[jobType])
        randOrder = list(range(numPops))
        random.shuffle(randOrder)

        #   Find goods available
        listPrices = self.getPriceList()

        popsDone = 0
        while not (popsDone == numPops):
            popsDone = 0

            for idx in randOrder:

                #   First, find randomly selected pop in 2D list
                jobType = 0
                listIdx = idx
                popSelected = False

                while not (popSelected):
                    if (listIdx >= len(self.listPops[jobType])):
                        listIdx -= len(self.listPops[jobType])
                        jobType += 1
                    else:
                        popSelected = True

                bought, boughtGoodType = self.listPops[jobType][listIdx].maximiseUtility(
                    listPrices)

                if (bought):
                    self.listGoodMarkets[boughtGoodType].buyLowest()
                    listPrices = self.getPriceList()
                else:
                    popsDone += 1

    def stepCloseMarkets(self):
        #   Give firms money from stalls
        for market in self.listGoodMarkets:
            for stall in market.listStalls:
                firmID = stall.firmID

                foundFirm = False
                for goodType in range(NUM_GOOD_TYPES):
                    if not foundFirm:
                        for firm in self.listFirms[goodType]:
                            if (firm.firmID == firmID):
                                firm.receiveRevenue(stall.funds, stall.sales, stall.qty)
                                foundFirm = True
                                break
                    else:
                        break
                            
    
    def stepCompanyTax(self):
        #   No company tax yet
        pass

    def stepReset(self):
        self.resetPops()
        self.resetFirms()
        self.resetLabourMarkets()
        self.resetGoodMarkets()

    def determineLabourDemand(self):
        # 1. Firms pay owners dividends
        # 2. Firms price goods competitively
        # 2. Firms determine labour demand and price
        # 3. Place available contracts in labour markets

        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:

                #   Firm pays its owner dividends
                for capitalist in self.listPops[JOB_CAPITALIST]:
                    if (firm.ownerID == capitalist.popID):
                        dividends = firm.payDividends()
                        capitalist.acceptDividends(dividends)
                        break

                #   Firm prices goods
                firm.updatePrice()

                #   Firm determines labour demand
                firm.determineLabour()

                #   Firm produces labour orders
                for jobType in range(NUM_JOB_TYPES-1):
                    firmID, vacancies, wage = firm.demandLabour(jobType)
                    self.listLabourMarkets[jobType].addOrder(firmID, vacancies, wage)

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
                    acceptedWage, firmID = self.listLabourMarkets[jobType].acceptHighest()
                    self.listPops[jobType][idx].acceptJob(acceptedWage)
                    highestWage = self.listLabourMarkets[jobType].findHighest()

    def settleLabour(self):    
        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:
                firmID = firm.firmID

                for jobType in range(NUM_JOB_TYPES-1):
                    supply = self.listLabourMarkets[jobType].supplyLabour(firmID)
                    firm.receiveLabour(jobType, supply)

        for jobType in range(NUM_JOB_TYPES-1):
            self.listLabourMarkets[jobType].close()

    def getPriceList(self):
        listPrices = []
        for goodType in range(NUM_GOOD_TYPES):
            price = self.listGoodMarkets[goodType].findLowest()
            listPrices.append(price)
        return listPrices

    def resetPops(self):
        numPops = 0
        avgUtils = 0
        for jobType in range(NUM_JOB_TYPES):
            for pop in self.listPops[jobType]:
                pop.consumeGoods()
                pop.reset()
                numPops += 1
                avgUtils += pop.utils
                pop.log()
        avgUtils /= numPops

        with open("simpleClosedEconomy/log/pops.txt", "a") as logFile:
            logFile.write("Avg. utils: " + "{:.2f}".format(avgUtils) + " \n")

    def resetFirms(self):
        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:
                firm.reset()
                firm.log()

    def resetLabourMarkets(self):
        for market in self.listLabourMarkets:
            market.reset()
            market.log()

    def resetGoodMarkets(self):
        for market in self.listGoodMarkets:
            market.reset()
            market.log()

    def monthlyPrices(self):
        listPrices = []

        for market in self.listGoodMarkets:
            listPrices.append(market.prevAvgPrice)

        return listPrices

    def monthlySales(self):
        listSales = []

        for market in self.listGoodMarkets:
            listSales.append(market.prevSales)

        return listSales

    def monthlyWages(self):
        listWages = []

        for market in self.listLabourMarkets:
            listWages.append(market.prevAvgWage)

        numCapitalists = len(self.listPops[JOB_CAPITALIST])
        avgCapitalistIncome = 0
        if (numCapitalists > 0):
            for capitalist in self.listPops[JOB_CAPITALIST]:
                avgCapitalistIncome += capitalist.prevIncome
            avgCapitalistIncome /= numCapitalists
        listWages.append(avgCapitalistIncome)

        return listWages

    def monthlyJobs(self):
        listHired = []

        for market in self.listLabourMarkets:
            listHired.append(market.prevTotalHires)

        numCapitalists = len(self.listPops[JOB_CAPITALIST])
        listHired.append(numCapitalists)

        return listHired

    def logHeader(self, month):
        with open("simpleClosedEconomy/log/jobs.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")

        with open("simpleClosedEconomy/log/sales.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")

        with open("simpleClosedEconomy/log/firms.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")

        with open("simpleClosedEconomy/log/pops.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")
