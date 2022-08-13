from .firm import *

class LabourMarket:
    def __init__(self, jobType, initWage=None, initSupply=None, initHired=None):
        self.jobType: int = jobType

        self.wage = INIT_WAGES[jobType]
        if not (initWage == None):
            self.wage = initWage
        
        self.prevSupply: int = INIT_POPULATION[jobType]
        if not (initSupply == None):
            self.prevSupply = initSupply
        
        self.prevHired: int = INIT_POPULATION[jobType]
        if not (initHired == None):
            self.prevHired: int = initHired

        self.currSupply: int = self.prevSupply
        self.currHired: int = self.prevHired

        self.currDividends = 0

    def setWage(self):
        labourEquilibrium = int((1 - NATURAL_UNEMPLOYMENT) * self.prevSupply)
        self.wage = (1 + MONTHLY_INFLATION) * self.wage
        if (self.prevHired > labourEquilibrium):
            self.wage = random.uniform(1, 1 + WAGE_VISCOSITY) * self.wage
        elif (self.prevHired == labourEquilibrium):
            self.wage = self.wage
        elif (self.prevHired < labourEquilibrium):
            self.wage = random.uniform(1 - WAGE_VISCOSITY, 1) * self.wage

        self.wage = round(self.wage, 2)

    def setSupply(self, supply):
        self.currSupply = supply

    def getWage(self):
        return self.wage

    def getNumHired(self):
        return self.currHired

    def labourAvailable(self):
        if (self.currSupply > self.currHired):
            return True
        else:
            return False

    def hire(self):
        self.currHired += 1

    def addDividends(self, dividends):
        self.currDividends += dividends

    def getTotDividends(self):
        return self.currDividends

    def reset(self):
        self.prevSupply = self.currSupply
        self.prevHired = self.currHired
        self.currSupply = 0
        self.currHired = 0
        self.currDividends = 0

    def log(self):
        with open("closedEconomy/log/jobs.txt", "a") as logFile:
            logFile.write(DICT_JOB_TITLES[self.jobType] + " Jobs: " + str(self.currHired) + "/" + 
            str(self.currSupply) + " hired at $" + "{:.2f}".format(self.wage) + "\n")