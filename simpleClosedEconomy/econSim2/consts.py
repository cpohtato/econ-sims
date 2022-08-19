from .imports import *

PRIVATE_SAVINGS_RATE = 0.0
FIRM_SAVINGS_RATE = 0.4
DIVIDEND_RATE = 0.05
WAGE_VISCOSITY = 0.03

TARGET_SURPLUS_PROD = 10

NUM_GOOD_TYPES = 2
TYPE_FOOD = 0
TYPE_ENERGY = 1

PROD_COST = [0.5, 0.5]
INIT_PRICE = [0.5, 0.5]

DICT_GOOD_NAMES = {
    TYPE_FOOD: "Food",
    TYPE_ENERGY: "Energy"
}

NUM_JOB_TYPES = 3
JOB_UNSKILLED = 0
JOB_SKILLED = 1
JOB_CAPITALIST = 2

JOB_PROD = [1, 2]
INIT_WAGES = [1, 2]

DICT_JOB_TITLES = {
    JOB_UNSKILLED: "Unskilled",
    JOB_SKILLED: "Skilled",
    JOB_CAPITALIST: "Capitalist"
}

INIT_POPULATION = [4, 0, 2]
INIT_SAVINGS = [2, 5, 10]
INIT_FIRMS = [2, 0]

MALE_FIRST_NAMES_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/male.txt", 'r')]
SURNAMES_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/surnames.txt", 'r')]
FOOD_COMPANY_NAME_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/food.txt", 'r')]
ENERGY_COMPANY_NAME_DATA = [line.strip() for line in open("simpleClosedEconomy/econSim2/names/energy.txt", 'r')]