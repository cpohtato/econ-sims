from econ_agents import *

class NationalEconomy:

    def __init__(self, initDemos: list[Demo], initFirms: list[list[Firm]], listProductivity: list[Double], 
    listInitAvgWages: list[Double]):

        """
        Initialisation function for a national economy

        Args:
            initDemos: List of initial demographic segments
        Returns:
        Raises:
        """

        self.listDemos = initDemos
        self.listFirms = initFirms
        self.listProductivity = listProductivity
        self.listInitAvgWages = listInitAvgWages

        self.listGoodMarkets: list[GoodMarket] = []
        for goodType in range(NUM_GOOD_TYPES):
            self.listGoodMarkets.append(GoodMarket(goodType))

        self.listLabourMarkets: list[LabourMarket] = []
        for jobType in range(NUM_JOB_TYPES):
            self.listLabourMarkets.append(LabourMarket(jobType, INIT_POPULATION[jobType], 
            self.listInitAvgWages[jobType] * INIT_POPULATION[jobType]))

    def stepDemoPromote(self):
        
        for demo in self.listDemos:
            #   Demo promote/demote
            #   Not implemented yet
            pass


    def stepDemoGrowth(self):
        #   Add/remove demos
        #   Not implemented yet
        pass

    def stepDemos(self):
        """
        Determines demo promotion and growth for a single step

        Args:
        Returns:
        Raises:
        """
        
        self.stepDemoPromote()
        self.stepDemoGrowth()

    def stepFirms(self):
        #   Firms enter/exit/expand/shrink
        #   Not implemented yet
        pass

    def stepLabour(self):
        #   Solve labour market
        #   Each firm determines labour demand, posts labour order
        #   Govt does the same
        #   Demos fulfil labour demand

        listAvgWages = []

        for market in self.listLabourMarkets:
            listAvgWages.append(market.findAvgWageAccepted())
            market.resetStats()

        #   Govt does it first

        for goodType in range(NUM_GOOD_TYPES):

            for firm in self.listFirms[goodType]:
                firm.determineLabour(listAvgWages, self.listProductivity)
                listLabourOrders = firm.produceLabourOrders()

                for labourOrder in listLabourOrders:
                    jobType = labourOrder.jobType
                    self.listLabourMarkets[jobType].addLabourOrder(labourOrder)

        #   Now that labour orders have been generated, demos pick contracts in random order
        listShuffleDemos = list(range(len(self.listDemos)))
        random.shuffle(listShuffleDemos)

        for idx in listShuffleDemos:
            demo = self.listDemos[idx]
            jobType = demo.jobType
            demo.pickContract(self.listLabourMarkets[jobType])

        self.logLabourMarkets()

        for market in self.listLabourMarkets:
            market.close(self.listFirms)

    def stepSubsidies(self):
        #   No govt subsidies yet
        pass

    def stepIncomeTax(self):
        #   No income tax yet
        pass

    def stepOpenMarkets(self):
        for market in self.listGoodMarkets:
            market.reset()

        for goodType in range(NUM_GOOD_TYPES):
            randomOrder = list(range(len(self.listFirms[goodType])))
            random.shuffle(randomOrder)
            for idx in randomOrder:
                self.listFirms[goodType][idx].produceGoods(self.listProductivity, self.listGoodMarkets)

    def stepPublicProcurement(self):
        #   Govt buys stuff
        pass

    def stepPrivateConsumption(self):
        #   Demos buy stuff until everyone is done
        randomOrder = list(range(len(self.listDemos)))
        random.shuffle(randomOrder)
        numDemos = len(self.listDemos)
        numDone = 0

        while not (numDone == numDemos):
            numDone = 0
            for idx in randomOrder:
                if not (self.listDemos[idx].buyMargin(self.listGoodMarkets)):
                    numDone += 1


    def stepCloseMarkets(self):
        
        for market in self.listGoodMarkets:
            market.close(self.listFirms)

        for goodType in range(NUM_GOOD_TYPES):
            for firm in self.listFirms[goodType]:
                firm.reset()

        for demo in self.listDemos:
            demo.reset()

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

        with open("closedEconomy/log/labourOrders.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")

        with open("closedEconomy/log/sellOrders.txt", "a") as logFile:
            logFile.write("\n")
            logFile.write("========================= MONTH " + str(month) + " =========================\n")
            logFile.write("\n")


        self.stepDemos()
        self.stepFirms()
        self.stepLabour()
        self.stepSubsidies()
        self.stepIncomeTax()
        self.stepOpenMarkets()
        self.stepPublicProcurement()
        self.stepPrivateConsumption()
        self.stepCloseMarkets()

        return True

    def logLabourMarkets(self):
        for market in self.listLabourMarkets:
            market.log()

    def logGoodMarkets(self):
        for market in self.listGoodMarkets:
            market.log()

    def monthlySales(self):
        monthlySales = []

        for market in self.listGoodMarkets:
            monthlySales.append(market.totalSales)

        return monthlySales

    def monthlyPrices(self):
        monthlyPrices = []

        for market in self.listGoodMarkets:
            monthlyPrices.append(market.avgPrice)

        return monthlyPrices

    def monthlyJobs(self):
        monthlyJobs = []

        for market in self.listLabourMarkets:
            monthlyJobs.append(market.contractsAccepted)

        return monthlyJobs

    def monthlyWages(self):
        monthlyWages = []

        for market in self.listLabourMarkets:
            monthlyWages.append(market.findAvgWageAccepted())

        return monthlyWages
