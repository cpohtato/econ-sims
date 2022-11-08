from econSim2 import *

SIM_LENGTH = 12

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

        plt.figure(1)
        plt.clf()
        plt.plot(arrTime[:month+1], arrPrices[:month+1, TYPE_FOOD], label="Food")
        plt.plot(arrTime[:month+1], arrPrices[:month+1, TYPE_ENERGY], label="Energy")
        plt.title("Market Prices")
        plt.xlabel("Month")
        plt.ylabel("Price")
        plt.xlim(1, SIM_LENGTH)
        plt.legend()

        plt.figure(2)
        plt.clf()
        plt.plot(arrTime[:month+1], arrSales[:month+1, TYPE_FOOD], label="Food")
        plt.plot(arrTime[:month+1], arrSales[:month+1, TYPE_ENERGY], label="Energy")
        plt.title("Monthly Sales")
        plt.xlabel("Month")
        plt.ylabel("Sales")
        plt.xlim(1, SIM_LENGTH)
        plt.legend()

        plt.figure(3)
        plt.clf()
        plt.plot(arrTime[:month+1], arrWages[:month+1, JOB_UNSKILLED], label="Unskilled")
        plt.plot(arrTime[:month+1], arrWages[:month+1, JOB_SKILLED], label="Skilled")
        plt.plot(arrTime[:month+1], arrWages[:month+1, JOB_CAPITALIST], label="Capitalist")
        plt.title("Monthly Wages")
        plt.xlabel("Month")
        plt.ylabel("Wage")
        plt.xlim(1, SIM_LENGTH)
        plt.legend()

        plt.figure(4)
        plt.clf()
        plt.plot(arrTime[:month+1], arrJobs[:month+1, JOB_UNSKILLED], label="Unskilled")
        plt.plot(arrTime[:month+1], arrJobs[:month+1, JOB_SKILLED], label="Skilled")
        plt.plot(arrTime[:month+1], arrJobs[:month+1, JOB_CAPITALIST], label="Capitalist")
        plt.title("Monthly Jobs")
        plt.xlabel("Month")
        plt.ylabel("Jobs")
        plt.xlim(1, SIM_LENGTH)
        plt.legend()

        plt.draw()
        plt.pause(0.001)
    
    plt.show()

if (__name__ == "__main__"):
    main()