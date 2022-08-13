from .govt import *

def wipeLogs():
    with open("closedEconomy/log/jobs.txt", "w") as logFile:
        logFile.write("")
        
    with open("closedEconomy/log/sales.txt", "w") as logFile:
        logFile.write("")

    with open("closedEconomy/log/firms.txt", "w") as logFile:
        logFile.write("")

def plotSim(arrPrices, arrSales, arrWages, arrJobs, arrTime):
    plt.figure(1)
    plt.plot(arrTime, arrPrices[:SIM_LENGTH, TYPE_PRODUCE], label="Produce")
    plt.plot(arrTime, arrPrices[:SIM_LENGTH, TYPE_ENERGY], label="Energy")
    plt.title("Market Prices")
    plt.xlabel("Month")
    plt.ylabel("Price")
    plt.xlim(1, SIM_LENGTH)
    plt.legend()

    plt.figure(2)
    plt.plot(arrTime, arrSales[:SIM_LENGTH, TYPE_PRODUCE], label="Produce")
    plt.plot(arrTime, arrSales[:SIM_LENGTH, TYPE_ENERGY], label="Energy")
    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.xlim(1, SIM_LENGTH)
    plt.legend()

    plt.figure(3)
    plt.plot(arrTime, arrWages[:SIM_LENGTH, JOB_MAGNATE], label="Magnate")
    plt.plot(arrTime, arrWages[:SIM_LENGTH, JOB_ADMINISTRATOR], label="Admin")
    plt.plot(arrTime, arrWages[:SIM_LENGTH, JOB_TECHNOLOGIST], label="Tech")
    plt.plot(arrTime, arrWages[:SIM_LENGTH, JOB_LABOURER], label="Labourer")
    plt.title("Monthly Wages")
    plt.xlabel("Month")
    plt.ylabel("Wage")
    plt.xlim(1, SIM_LENGTH)
    plt.legend()

    plt.figure(4)
    plt.plot(arrTime, arrJobs[:SIM_LENGTH, JOB_MAGNATE], label="Magnate")
    plt.plot(arrTime, arrJobs[:SIM_LENGTH, JOB_ADMINISTRATOR], label="Admin")
    plt.plot(arrTime, arrJobs[:SIM_LENGTH, JOB_TECHNOLOGIST], label="Tech")
    plt.plot(arrTime, arrJobs[:SIM_LENGTH, JOB_LABOURER], label="Labourer")
    plt.title("Monthly Jobs")
    plt.xlabel("Month")
    plt.ylabel("Jobs")
    plt.xlim(1, SIM_LENGTH)
    plt.legend()

    plt.show()