from .utils import *

class Firm():
    def __init__(self, firmID: int, goodType: int):
        self.firmID: int = firmID
        self.goodType: int = goodType
        self.ownerID: int = None
        self.name: str = None

    def generateName(self, surname: str):
        if (self.goodType == TYPE_FOOD):
            companyName: str = random.choice(FOOD_COMPANY_NAME_DATA)
        elif (self.goodType == TYPE_ENERGY):
            companyName: str = random.choice(ENERGY_COMPANY_NAME_DATA)

        self.name = surname + " " + companyName