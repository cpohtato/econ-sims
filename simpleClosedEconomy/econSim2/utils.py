from .consts import *

def wipeLogs():
    with open("log/jobs.txt", "w") as logFile:
        logFile.write("")
        
    with open("log/sales.txt", "w") as logFile:
        logFile.write("")

    with open("log/firms.txt", "w") as logFile:
        logFile.write("")

    with open("log/pops.txt", "w") as logFile:
        logFile.write("")

def generatePopName():
    popName = random.choice(MALE_FIRST_NAMES_DATA) + " " + random.choice(SURNAMES_DATA)
    popName = popName.rstrip()
    return popName

# GEN_NAMES = 10
# COMPOUND_PROB = 0.2

# def genNames():

#     maleFirstData = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/male.txt", 'r')]
#     surnameData = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/surnames.txt", 'r')]
#     companyData = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/metal.txt", 'r')]

#     for name in range(GEN_NAMES):
#         if (random.random() < COMPOUND_PROB):
#             companyName = "%s-%s %s"%(random.choice(surnameData), random.choice(surnameData), random.choice(companyData))
#         else:
#             companyName = str(random.choice(surnameData)) + " " + str(random.choice(companyData))
#         print(companyName)

        # personName = random.choice(maleFirstData) + " " + random.choice(surnameData)
        # print(personName)


