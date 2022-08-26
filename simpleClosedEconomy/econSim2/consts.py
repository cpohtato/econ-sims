from .imports import *

PRIVATE_SAVINGS_RATE = 0.0
FIRM_SAVINGS_RATE = 0.5
DIVIDEND_RATE = 0.05
WAGE_VISCOSITY = 0.03
PRICE_VISCOSITY = 0.04

TARGET_SURPLUS = 0.1

NUM_GOOD_TYPES = 2
TYPE_FOOD = 0
TYPE_ENERGY = 1

PROD_COST = [0.1, 0.05]
INIT_PRICE = [0.07, 0.07]

GOOD_PREF_MEAN = [1, 1]
GOOD_PREF_NORM_STD_DEV = [0.2, 0.2]

RESERVE_WAGE_MEAN =         [[4, 0],
                             [4, 0],
                             [4, 0]]
RESERVE_WAGE_NORM_STD_DEV = [[0.5, 0],
                             [0.5, 0],
                             [0.5, 0]]
RESERVE_WAGE_MIN =          [[1, 0],
                             [1, 0],
                             [1, 0]]

DICT_GOOD_NAMES = {
    TYPE_FOOD: "Food",
    TYPE_ENERGY: "Energy"
}

NUM_JOB_TYPES = 3
JOB_UNSKILLED = 0
JOB_SKILLED = 1
JOB_CAPITALIST = 2

#   Set skilled labour to zero productivity for now
JOB_PROD_MEAN = [1, 0]
JOB_PROD_NORM_STD_DEV = [0.3, 0]
SCALE_FACTOR = 5

INIT_WAGES = [0.6, 2]

DICT_JOB_TITLES = {
    JOB_UNSKILLED: "Unskilled",
    JOB_SKILLED: "Skilled",
    JOB_CAPITALIST: "Capitalist"
}

INIT_POPULATION = [50, 0, 10]
INIT_SAVINGS = [2, 5, 10]
INIT_FIRMS = [5, 5]

MALE_FIRST_NAMES_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/male.txt", 'r')]
SURNAMES_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/surnames.txt", 'r')]
FOOD_COMPANY_NAME_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/food.txt", 'r')]
ENERGY_COMPANY_NAME_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/energy.txt", 'r')]