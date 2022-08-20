from .utils import *

class Pop():
    def __init__(self, popID: int, jobType: int, initSavings: float):
        self.popID: int = popID
        self.jobType: int = jobType
        self.funds: float = initSavings
        self.firstName: str = (random.choice(MALE_FIRST_NAMES_DATA)).rstrip()
        self.surname: str = (random.choice(SURNAMES_DATA)).rstrip()
        self.ownFirmID: int = None

        self.reserveWageGoods: list[float] = []
        for goodType in range(NUM_GOOD_TYPES):
            minGood = random.gauss(RESERVE_WAGE_MEAN[self.jobType][goodType],
            RESERVE_WAGE_NORM_STD_DEV[jobType][goodType] * RESERVE_WAGE_NORM_STD_DEV[jobType]
            [goodType])

            if (minGood < RESERVE_WAGE_MIN[jobType][goodType]):
                minGood = RESERVE_WAGE_MIN[jobType][goodType]

            self.reserveWageGoods.append(minGood)

        self.employed: bool = False
        self.currIncome: float = 0.0

    def getFullName(self):
        fullName: str = self.firstName + " " + self.surname
        return fullName

    def offerWage(self, highestWage: float, listGoodPrices: list[float]):
        reserveWage = 0

        for goodType in range(NUM_GOOD_TYPES):
            reserveWage += listGoodPrices[goodType] * self.reserveWageGoods[goodType]

        if (highestWage >= reserveWage):
            #   Return true if highest wage available is acceptable
            return True
        else:
            #   Otherwise decline job
            return False

    def acceptJob(self, wage: float):
        self.employed = True
        self.currIncome = wage
        self.funds += wage

    def acceptDividends(self, dividends: float):
        self.currIncome = dividends
        self.funds += dividends
