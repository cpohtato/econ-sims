from econSim import *

def main():
    wipeLogs()

    natEcon = NationalEconomy()

    arrSales = np.zeros((SIM_LENGTH, NUM_GOOD_TYPES))
    arrPrices = np.zeros((SIM_LENGTH, NUM_GOOD_TYPES))
    arrJobs = np.zeros((SIM_LENGTH, NUM_JOB_TYPES))
    arrWages = np.zeros((SIM_LENGTH, NUM_JOB_TYPES))
    arrTime = list(range(1, SIM_LENGTH + 1))

    for month in range(SIM_LENGTH):
        print("Month " + str(month + 1))
        if not (natEcon.monthStep(month + 1)):
            print("Error")

        arrPrices[month] = natEcon.monthlyPrices()
        arrSales[month] = natEcon.monthlySales()
        arrWages[month] = natEcon.monthlyWages()
        arrJobs[month] = natEcon.monthlyJobs()   

    print("Sim complete")

    with open("closedEconomy/log/pricesExcel.txt", "w") as logFile:
        for month in range(SIM_LENGTH):
            logFile.write(str(month + 1) + " " + str(arrPrices[month, TYPE_PRODUCE]) + " " + 
            str(arrPrices[month, TYPE_ENERGY]) + "\n")

    with open("closedEconomy/log/wagesExcel.txt", "w") as logFile:
        for month in range(SIM_LENGTH):
            logFile.write(str(month + 1) + " " + str(arrWages[month, JOB_MAGNATE]) + " " + 
            str(arrWages[month, JOB_ADMINISTRATOR]) + " " + str(arrWages[month, JOB_TECHNOLOGIST])
            + " " + str(arrWages[month, JOB_LABOURER]) + "\n")

    plotSim(arrPrices, arrSales, arrWages, arrJobs, arrTime)



if (__name__ == "__main__"):
    main()
