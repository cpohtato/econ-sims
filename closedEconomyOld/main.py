#   Model of national economy (closed for now)
#   Includes population, industrial firms, markets and government

from nat_econ import *
import matplotlib.pyplot as plt

SIM_LENGTH = 12

INIT_NATIONAL_PRODUCTIVITY = [10.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0]
INIT_AVG_WAGES = [10.0, 5.0, 5.0, 2.0, 2.0, 2.0, 2.0]


def main():
    wipeLogs()
    
    initDemos = generateInitDemos()

    initFirms = generateInitFirms()

    natEcon = NationalEconomy(initDemos, initFirms, INIT_NATIONAL_PRODUCTIVITY, INIT_AVG_WAGES)

    arrSales = np.zeros((SIM_LENGTH, NUM_GOOD_TYPES))
    arrPrices = np.zeros((SIM_LENGTH, NUM_GOOD_TYPES))
    arrJobs = np.zeros((SIM_LENGTH, NUM_JOB_TYPES))
    arrWages = np.zeros((SIM_LENGTH, NUM_JOB_TYPES))
    arrTime = list(range(1, SIM_LENGTH + 1))

    for month in range(SIM_LENGTH):
        print("Month " + str(month + 1))
        if not (natEcon.monthStep(month + 1)):
            print("Error")

        arrSales[month] = natEcon.monthlySales()
        arrPrices[month] = natEcon.monthlyPrices()
        arrJobs[month] = natEcon.monthlyJobs()
        arrWages[month] = natEcon.monthlyWages()

    print("Sim complete")

    plt.figure(1)
    plt.plot(arrTime, arrPrices[:SIM_LENGTH, TYPE_PRODUCE], label="Produce")
    plt.plot(arrTime, arrPrices[:SIM_LENGTH, TYPE_ENERGY], label="Energy")
    plt.title("Average Market Price")
    plt.xlabel("Month")
    plt.ylabel("Price")
    plt.legend()

    plt.figure(2)
    plt.plot(arrTime, arrSales[:SIM_LENGTH, TYPE_PRODUCE], label="Produce")
    plt.plot(arrTime, arrSales[:SIM_LENGTH, TYPE_ENERGY], label="Energy")
    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.legend()

    plt.figure(3)
    plt.plot(arrTime, arrWages[:SIM_LENGTH, JOB_MAGNATE], label="Magnate")
    plt.plot(arrTime, arrWages[:SIM_LENGTH, JOB_ADMINISTRATOR], label="Admin")
    plt.plot(arrTime, arrWages[:SIM_LENGTH, JOB_TECHNOLOGIST], label="Tech")
    plt.plot(arrTime, arrWages[:SIM_LENGTH, JOB_LABOURER], label="Labourer")
    plt.title("Monthly Wages")
    plt.xlabel("Month")
    plt.ylabel("Wage")
    plt.legend()

    plt.figure(4)
    plt.plot(arrTime, arrJobs[:SIM_LENGTH, JOB_MAGNATE], label="Magnate")
    plt.plot(arrTime, arrJobs[:SIM_LENGTH, JOB_ADMINISTRATOR], label="Admin")
    plt.plot(arrTime, arrJobs[:SIM_LENGTH, JOB_TECHNOLOGIST], label="Tech")
    plt.plot(arrTime, arrJobs[:SIM_LENGTH, JOB_LABOURER], label="Labourer")
    plt.title("Monthly Jobs")
    plt.xlabel("Month")
    plt.ylabel("Jobs")
    plt.legend()

    plt.show()




if (__name__ == "__main__"):
    main()