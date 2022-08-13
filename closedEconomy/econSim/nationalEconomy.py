from .utils import *

class NationalEconomy:
    def __init__(self, initPops: list[list[Pop]]=None, initFirms: list[list[Firm]]=None,
    initLabourMarkets: list[LabourMarket]=None, initGoodMarkets: list[GoodMarket]=None):

        self.listPops: list[list[Pop]] = [[]]
        if (initPops == None):
            self.listPops = self.generateInitPops()
        else:
            self.listPops = initPops
        
        self.listFirms: list[list[Firm]] = [[]]
        if (initFirms == None):
            self.listFirms = self.generateInitFirms()
        else:
            self.listFirms = initFirms

        self.listLabourMarkets: list[LabourMarket] = []
        if (initLabourMarkets == None):
            self.listLabourMarkets = self.generateInitLabourMarkets()
        else:
            self.listLabourMarkets = initLabourMarkets

        self.listGoodMarkets: list[GoodMarket] = []
        if (initGoodMarkets == None):
            self.listGoodMarkets = self.generateInitGoodMarkets()
        else:
            self.listGoodMarkets = initGoodMarkets

    def generateInitPops(self):
        initPops: list[list[Pop]] = [[] for i in range(NUM_JOB_TYPES)]

        for jobType in range(NUM_JOB_TYPES):
            for pop in range(INIT_POPULATION[jobType]):
                initPops[jobType].append(Pop(jobType, INIT_WAGES[jobType]))

        return initPops

    def generateInitFirms(self):
        initFirms: list[list[Firm]] = [[] for i in range(NUM_GOOD_TYPES)]

        for goodType in range(NUM_GOOD_TYPES):
            for firm in range(INIT_FIRMS[goodType]):
                initFirms[goodType].append(Firm(goodType, initMachinery=INIT_MACHINERY*firm, 
                initSpecMachinery=INIT_SPEC_MACHINERY*firm))

        return initFirms

    def generateInitLabourMarkets(self):
        initLabourMarkets: list[LabourMarket] = []

        for jobType in range(NUM_JOB_TYPES):
            initLabourMarkets.append(LabourMarket(jobType))

        return initLabourMarkets

    def generateInitGoodMarkets(self):
        initGoodMarkets: list[GoodMarket] = []

        for goodType in range(NUM_GOOD_TYPES):
            initGoodMarkets.append(GoodMarket(goodType))

        return initGoodMarkets

    def stepPops(self):

        listWages = []
        for market in self.listLabourMarkets:
            listWages.append(market.getWage())

        listPopChange = [0] * NUM_JOB_TYPES
        listDemote = [0] * NUM_JOB_TYPES
        listPops = [0] * NUM_JOB_TYPES
        for jobType in range(NUM_JOB_TYPES):
            listPops[jobType] = len(self.listPops[jobType])

            #   Calculate job change based on attrition
            if (jobType < 3):
                delta = listPops[jobType] * POP_ATTRITION
                chance = delta % 1
                if (chance != 0):
                    if (random.random() < chance):
                        delta = math.ceil(delta)
                    else:
                        delta = math.floor(delta)
                listPopChange[jobType] -= delta
                listDemote[jobType] += delta
                listPopChange[JOB_LABOURER] += delta

        #   Admin to magnate
        if (listPops[JOB_ADMINISTRATOR] + listPopChange[JOB_ADMINISTRATOR] > 0):
            wageRatio = listWages[JOB_MAGNATE]/listWages[JOB_ADMINISTRATOR]
            delta = listPops[JOB_ADMINISTRATOR] * (JOB_MOBILITY * wageRatio) / MAGNATE_EDUCATION

            chance = delta % 1
            if (chance != 0):
                if (random.random() < chance):
                    delta = math.ceil(delta)
                else:
                    delta = math.floor(delta)

            if (listPops[JOB_ADMINISTRATOR] + listPopChange[JOB_ADMINISTRATOR] < delta):
                delta = listPops[JOB_ADMINISTRATOR] + listPopChange[JOB_ADMINISTRATOR]
            listPopChange[JOB_ADMINISTRATOR] -= delta
            listPopChange[JOB_MAGNATE] += delta
            adminToMagnate = delta

        #   Lab to admin
        if (listPops[JOB_LABOURER] + listPopChange[JOB_LABOURER] > 0):
            wageRatio = listWages[JOB_ADMINISTRATOR]/listWages[JOB_LABOURER]
            delta = listPops[JOB_LABOURER] * (JOB_MOBILITY * wageRatio) / ADMIN_EDUCATION

            chance = delta % 1
            if (chance != 0):
                if (random.random() < chance):
                    delta = math.ceil(delta)
                else:
                    delta = math.floor(delta)

            if (listPops[JOB_LABOURER] + listPopChange[JOB_LABOURER] < delta):
                delta = listPops[JOB_LABOURER] + listPopChange[JOB_LABOURER]
            listPopChange[JOB_LABOURER] -= delta
            listPopChange[JOB_ADMINISTRATOR] += delta
            labToAdmin = delta

        #   Lab to tech
        if (listPops[JOB_LABOURER] + listPopChange[JOB_LABOURER] > 0):
            wageRatio = listWages[JOB_TECHNOLOGIST]/listWages[JOB_LABOURER]
            delta = listPops[JOB_LABOURER] * (JOB_MOBILITY * wageRatio) / TECH_EDUCATION

            chance = delta % 1
            if (chance != 0):
                if (random.random() < chance):
                    delta = math.ceil(delta)
                else:
                    delta = math.floor(delta)

            if (listPops[JOB_LABOURER] + listPopChange[JOB_LABOURER] < delta):
                delta = listPops[JOB_LABOURER] + listPopChange[JOB_LABOURER]
            listPopChange[JOB_LABOURER] -= delta
            listPopChange[JOB_TECHNOLOGIST] += delta
            labToTech = delta

        for jobType in range(NUM_JOB_TYPES):
            while (listDemote[jobType] > 0):
                randIdx = random.randint(0, len(self.listPops[jobType])-1)
                popped = self.listPops[jobType].pop(randIdx)
                popped.jobType = JOB_LABOURER
                self.listPops[JOB_LABOURER].append(popped)
                listDemote[jobType] -= 1

        for i in range(adminToMagnate):
            randIdx = random.randint(0, len(self.listPops[JOB_ADMINISTRATOR])-1)
            popped = self.listPops[JOB_ADMINISTRATOR].pop(randIdx)
            popped.studying = MAGNATE_EDUCATION
            popped.jobType = JOB_MAGNATE
            self.listPops[JOB_MAGNATE].append(popped)

        for i in range(labToAdmin):
            randIdx = random.randint(0, len(self.listPops[JOB_LABOURER])-1)
            popped = self.listPops[JOB_LABOURER].pop(randIdx)
            popped.studying = ADMIN_EDUCATION
            popped.jobType = JOB_ADMINISTRATOR
            self.listPops[JOB_ADMINISTRATOR].append(popped)

        for i in range(labToTech):
            randIdx = random.randint(0, len(self.listPops[JOB_LABOURER])-1)
            popped = self.listPops[JOB_LABOURER].pop(randIdx)
            popped.studying = TECH_EDUCATION
            popped.jobType = JOB_TECHNOLOGIST
            self.listPops[JOB_TECHNOLOGIST].append(popped)

        # listPopsNew = [0] * NUM_JOB_TYPES
        # for jobType in range(NUM_JOB_TYPES):
        #     listPopsNew[jobType] = len(self.listPops[jobType])

        students = 0
        for jobType in range(NUM_JOB_TYPES):
            for pop in self.listPops[jobType]:
                if (pop.studying > 0):
                    students += 1

        print(str(students) + " students")
                
    def stepFirms(self):
        #   No firm entry/growth yet
        pass

    def setLabourWages(self):
        for market in self.listLabourMarkets:
            market.setWage()

    def setLabourSupply(self):
        for market in self.listLabourMarkets:
            supply = 0
            jobType = market.jobType
            for pop in self.listPops[jobType]:
                if (pop.studying == 0):
                    supply += 1
            market.setSupply(supply)

    def getNumFirms(self):
        numFirms = 0
        for goodType in range(NUM_GOOD_TYPES):
            numFirms += len(self.listFirms[goodType])
        return numFirms

    def demandLabour(self):
        #   Indicates if hiring from each job market is even possible
        labourAvailable = []
        for market in self.listLabourMarkets:
            if (market.labourAvailable()):
                labourAvailable.append(1)
            else:
                labourAvailable.append(-1)

        #   Get wages for each job market
        listWages = []
        for labourMarket in self.listLabourMarkets:
            listWages.append(labourMarket.getWage())

        #   Get prices for each good type
        listPrices = []
        for goodMarket in self.listGoodMarkets:
            listPrices.append(goodMarket.getPrice())

        #   Govt does not hire any labour yet

        #   Private firms hire labour in random order
        #   First find total number of firms, then randomise order
        numFirms = self.getNumFirms()
        randOrder = list(range(numFirms))
        random.shuffle(randOrder)

        firmsDone = 0
        while not (firmsDone == numFirms):
            firmsDone = 0

            for idx in randOrder:
                #   First, find randomly selected firm in 2D list
                goodType = 0
                listIdx = idx
                firmSelected = False

                while not (firmSelected):
                    if (listIdx >= len(self.listFirms[goodType])):
                        listIdx -= len(self.listFirms[goodType])
                        goodType += 1
                    else:
                        firmSelected = True

                hired, hiredJobType = self.listFirms[goodType][listIdx].demandLabour(listWages,
                labourAvailable, listPrices)
                
                if (hired):
                    self.listLabourMarkets[hiredJobType].hire()

                    if (hiredJobType == JOB_MAGNATE):
                        dividends = self.listFirms[goodType][listIdx].payDividends()
                        self.listLabourMarkets[hiredJobType].addDividends(dividends)

                    if not (self.listLabourMarkets[hiredJobType].labourAvailable()):
                        labourAvailable[hiredJobType] = -1
                else:
                    #   If selected firm did not hire then it is done with labour markets
                    firmsDone += 1

    def closeLabourMarkets(self):
        for jobType in range(NUM_JOB_TYPES):
            numHired = self.listLabourMarkets[jobType].getNumHired()
            wage = self.listLabourMarkets[jobType].getWage()

            if (jobType == JOB_MAGNATE):
                if (numHired > 0):
                    dividendPortion = self.listLabourMarkets[jobType].getTotDividends()/numHired
                else:
                    dividendPortion = 0
            else:
                dividendPortion = 0

            randOrder = list(range(numHired))
            random.shuffle(randOrder)

            for idx in randOrder:
                if (numHired == 0):
                    break
                else:
                    self.listPops[jobType][idx].remunerate(wage + dividendPortion)
                    numHired -= 1

    def stepLabour(self):
        self.setLabourWages()
        self.setLabourSupply()
        self.demandLabour()
        self.closeLabourMarkets()
        self.logLabourMarkets()

    def stepSubsidies(self):
        #   No subsidies yet
        pass

    def stepIncomeTax(self):
        #   No taxes yet
        pass

    def stepOpenMarkets(self):
        #   Firms buy inputs
        #   Firms create outputs using productivity
        #   Firms tell markets how many goods they hold
        
        listPrices = []
        for market in self.listGoodMarkets:
            market.setPrice()
            listPrices.append(market.getPrice())

        for goodType in range(NUM_GOOD_TYPES):
            listAvailable = []
            for market in self.listGoodMarkets:
                listAvailable.append(market.getAvailable())

            randOrder = list(range(len(self.listFirms[goodType])))
            random.shuffle(randOrder)

            for idx in randOrder:
                qtyProduced, qtyTotal = self.listFirms[goodType][idx].produceGoods(listPrices, 
                listAvailable)

                #   Firms don't consume inputs yet
                #   Implement later

                self.listGoodMarkets[goodType].addGoods(qtyProduced, qtyTotal)

            # print(DICT_GOOD_NAMES[goodType] + " Market: " + str(self.listGoodMarkets[goodType].
            # getAvailable()) + " units @ $" + str(self.listGoodMarkets[goodType].getPrice()))

    def stepPublicProcurement(self):
        #   No public procurement yet
        pass

    def stepPrivateConsumption(self):
        #   Consumers perform utility maximisation

        listPrices = []
        listAvailable = []
        for market in self.listGoodMarkets:
            listPrices.append(market.getPrice())
            listAvailable.append(market.getAvailable())

        numPops = 0
        for jobType in range(NUM_JOB_TYPES):
            numPops += len(self.listPops[jobType])
            for pop in self.listPops[jobType]:
                pop.saveMoney()

        randOrder = list(range(numPops))
        random.shuffle(randOrder)

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
                    listPrices, listAvailable)

                if (bought):
                    self.listGoodMarkets[boughtGoodType].registerSale()
                    listAvailable[boughtGoodType] -= 1
                else:
                    popsDone += 1

    def stepCloseMarkets(self):
        #   Sales will be allocated on the basis of production first
        #   Remaining sales will be allocated according to inventory size
        #   Remaining sales will be randomly allocated
        for goodType in range(NUM_GOOD_TYPES):
            price = self.listGoodMarkets[goodType].getPrice()
            totalSales = self.listGoodMarkets[goodType].getSold()
            totalProduced = self.listGoodMarkets[goodType].getProduced()
            totalSupply = self.listGoodMarkets[goodType].getSupply()

            if (totalProduced > 0):
                ratio = totalSales/totalProduced
            else:
                ratio = 0

            salesRemaining = totalSales

            if (ratio > 1):
                for firm in self.listFirms[goodType]:
                    qtySold = int(firm.getProduced())
                    firm.makeSale(qtySold, price)
                    salesRemaining -= qtySold

                invRatio = salesRemaining/(totalSupply - totalProduced)
                for firm in self.listFirms[goodType]:
                    qtySold = int(firm.getAvailable() * invRatio)
                    firm.makeSale(qtySold, price)
                    salesRemaining -= qtySold
                        
            else:
                for firm in self.listFirms[goodType]:
                    qtySold = int(firm.getProduced() * ratio)
                    firm.makeSale(qtySold, price)

            numFirms = len(self.listFirms[goodType])
            while (salesRemaining > 0):
                numDone = 0
                randOrder = list(range(numFirms))
                random.shuffle(randOrder)
                for randIdx in randOrder:
                    if (self.listFirms[goodType][randIdx].getAvailable() > 1):
                        self.listFirms[goodType][randIdx].makeSale(1, price)
                        salesRemaining -= 1

                        if (salesRemaining < 1):
                            break
                    else:
                        numDone += 1
                
                if (numDone == numFirms):
                    break

        self.logGoodMarkets()
        self.logFirms()

    def reset(self):
        for jobType in range(NUM_JOB_TYPES):
            for pop in self.listPops[jobType]:
                pop.reset()

        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:
                firm.reset()

        for lMarket in self.listLabourMarkets:
            lMarket.reset()

        for gMarket in self.listGoodMarkets:
            gMarket.reset()

    def monthStep(self, month):

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
        # 6. Goods are produced and placed in markets
        #
        # 7. Govt buys goods
        #
        # 8. Population buys goods
        #
        # 9. Markets close, govt collects company tax

        self.logHeader(month)

        self.reset()
        self.stepPops()
        self.stepFirms()
        self.stepLabour()
        self.stepSubsidies()
        self.stepIncomeTax()
        self.stepOpenMarkets()
        self.stepPublicProcurement()
        self.stepPrivateConsumption()
        self.stepCloseMarkets() 

        return True

    def monthlyPrices(self):
        listPrices = []

        for market in self.listGoodMarkets:
            listPrices.append(market.getPrice())

        return listPrices

    def monthlySales(self):
        listSales = []

        for market in self.listGoodMarkets:
            listSales.append(market.getSold())

        return listSales

    def monthlyWages(self):
        listWages = []

        for market in self.listLabourMarkets:
            listWages.append(market.getWage())

        return listWages

    def monthlyJobs(self):
        listHired = []

        for market in self.listLabourMarkets:
            listHired.append(market.getNumHired())

        return listHired

    def logHeader(self, month):
        with open("closedEconomy/log/jobs.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")

        with open("closedEconomy/log/sales.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")

        with open("closedEconomy/log/firms.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")

    def logLabourMarkets(self):
        # for market in self.listLabourMarkets:
        #     print(DICT_JOB_TITLES[market.jobType] + " Market: " + str(market.currHired) + "/" +
        #     str(market.currSupply) + " hired")

        # for goodType in range(NUM_GOOD_TYPES):
        #     for firm in self.listFirms[goodType]:
        #         print(firm.listEmployees)
        #         unitsProduced = int(firm.getProd() / GOOD_COST[firm.goodType])
        #         cost = firm.getCurrExp()
        #         profit = unitsProduced * INIT_PRICE[firm.goodType] - cost
        #         print(str(unitsProduced) + " units at $" + "{:.2f}".format(INIT_PRICE[firm.goodType]))
        #         print("Profit: " + "{:.2f}".format(profit))
        #         print()

        for market in self.listLabourMarkets:
            market.log()
        with open("closedEconomy/log/jobs.txt", "a") as logFile:
            logFile.write("\n")

    def logGoodMarkets(self):
        for market in self.listGoodMarkets:
            market.log()
        with open("closedEconomy/log/sales.txt", "a") as logFile:
            logFile.write("\n")

    def logFirms(self):
        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:
                firm.log()
        with open("closedEconomy/log/firms.txt", "a") as logFile:
            logFile.write("")