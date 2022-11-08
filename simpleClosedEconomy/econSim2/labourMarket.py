from .pop import *
from .firm import *

class LabourOrder():
    def __init__(self, firmID: int, vacancies: int, wage: float):
        self.firmID: int = firmID
        self.totalVacancies: int = vacancies
        self.wage: float = wage
        self.accepted: int = 0

        self.prevAvgWage: float = 0.0
        self.prevTotalHires: int = 0

    def getVacanciesRemaining(self):
        return self.totalVacancies - self.accepted

    def accept(self):
        if (self.accepted < self.totalVacancies):
            self.accepted += 1
        else:
            print("Error: no more vacancies to be accepted")

class LabourMarket():
    def __init__(self, jobType: int):
        self.jobType: int = jobType
        self.listLabourOrders: list[LabourOrder] = []
        self.prevAvgWage = 0
        self.prevTotalHires = 0
        self.prevTotalOpen = 0

    def addOrder(self, firmID: int, vacancies: int, wage: int):
        newOrder = LabourOrder(firmID, vacancies, wage)
        self.listLabourOrders.append(newOrder)

    def findHighest(self):
        highestWage: float = 0

        for order in self.listLabourOrders:
            if (order.getVacanciesRemaining() > 0):
                if (order.wage > highestWage):
                    highestWage = order.wage

        return highestWage

    def acceptHighest(self):
        highestWage: float = 0
        # highestWageIdx: int = None
        highestWageFirmID: int = None

        for idx in range(len(self.listLabourOrders)):
            if (self.listLabourOrders[idx].getVacanciesRemaining() > 0):
                if (self.listLabourOrders[idx].wage > highestWage):
                    highestWage = self.listLabourOrders[idx].wage
                    # highestWageIdx = idx
                    highestWageFirmID = self.listLabourOrders[idx].firmID
                    self.listLabourOrders[idx].accept()
                    break

        return highestWage, highestWageFirmID

    def supplyLabour(self, firmID: int):
        for order in self.listLabourOrders:
            if (firmID == order.firmID):
                supply = order.accepted
                return supply

        return 0

    def close(self):
        self.prevAvgWage = 0
        self.prevTotalHires = 0
        self.prevTotalOpen = 0
        for order in self.listLabourOrders:
            self.prevTotalHires += order.accepted
            self.prevAvgWage += order.accepted * order.wage
            self.prevTotalOpen += order.totalVacancies
        
        if (self.prevTotalHires == 0):
            if (self.prevTotalOpen > 0):
                self.prevAvgWage /= self.prevTotalOpen
            else:
                self.prevAvgWage = 0
        else:
            self.prevAvgWage /= self.prevTotalHires

        self.listLabourOrders = []

    def reset(self):
        pass

    def log(self):
        with open("log/jobs.txt", "a") as logFile:
            logFile.write(DICT_JOB_TITLES[self.jobType] + " Jobs: " + str(self.prevTotalHires) + 
            "/" + str(self.prevTotalOpen) + " hired at $" + "{:.2f}".format(self.prevAvgWage) + 
            "\n")
        

        