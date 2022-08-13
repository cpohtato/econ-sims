import random
from tkinter import FIRST
from tokenize import String

GEN_NAMES = 10
COMPOUND_PROB = 0.2

def main():
    maleFirstData = [line.strip() for line in open("simpleClosedEconomy/econSim-2/names/male.txt", 'r')]
    surnameData = [line.strip() for line in open("simpleClosedEconomy/econSim-2/names/surnames.txt", 'r')]
    companyData = [line.strip() for line in open("simpleClosedEconomy/econSim-2/names/energy.txt", 'r')]

    for name in range(GEN_NAMES):
        if (random.random() < COMPOUND_PROB):
            companyName = "%s-%s %s"%(random.choice(surnameData), random.choice(surnameData), random.choice(companyData))
        else:
            companyName = str(random.choice(surnameData)) + " " + str(random.choice(companyData))
        print(companyName)

if (__name__ == "__main__"):
    main()