from .pop import *
from .firm import *

class LabourOrder():
    def __init__(self, firmID: int, vacancies: int, wage: float):
        self.firmID: int = firmID
        self.totalVacancies: int = vacancies
        self.wage: float = wage
        self.accepted: int = 0

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
        highestWageIdx: int = None
        highestWageFirmID: int = None

        for idx in range(len(self.listLabourOrders)):
            if (self.listLabourOrders[idx].getVacanciesRemaining() > 0):
                if (self.listLabourOrders[idx].wage > highestWage):
                    highestWage = self.listLabourOrders[idx].wage
                    highestWageIdx = idx
                    highestWageFirmID = self.listLabourOrders[idx].firmID
                    self.listLabourOrders[idx].accept()

        return highestWage

        