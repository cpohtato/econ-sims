from .imports import *

NUM_GOOD_TYPES = 2
TYPE_FOOD = 0
TYPE_ENERGY = 1

NUM_JOB_TYPES = 3
JOB_UNSKILLED = 0
JOB_SKILLED = 1
JOB_CAPITALIST = 2

DICT_JOB_TITLES = {
    JOB_UNSKILLED: "Unskilled",
    JOB_SKILLED: "Skilled",
    JOB_CAPITALIST: "Capitalist"
}

INIT_POPULATION = [4, 0, 4]
INIT_SAVINGS = [2, 5, 10]
INIT_FIRMS = [2, 3]

MALE_FIRST_NAMES_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/male.txt", 'r')]
SURNAMES_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/surnames.txt", 'r')]
FOOD_COMPANY_NAME_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/food.txt", 'r')]
ENERGY_COMPANY_NAME_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/energy.txt", 'r')]