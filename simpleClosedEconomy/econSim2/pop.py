from .utils import *

class Pop():
    def __init__(self, popID: int, jobType: int, initSavings: float):
        self.popID: int = popID
        self.jobType: int = jobType
        self.funds: float = initSavings
        self.firstName: str = (random.choice(MALE_FIRST_NAMES_DATA)).rstrip()
        self.surname: str = (random.choice(SURNAMES_DATA)).rstrip()
        self.ownFirmID: int = None

    def getFullName(self):
        fullName: str = self.firstName + " " + self.surname
        return fullName
