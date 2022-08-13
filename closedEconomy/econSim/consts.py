from .imports import *

SIM_LENGTH = 256

WAGE_VISCOSITY = 0.02
PRICE_VISCOSITY = 0.04
NATURAL_UNEMPLOYMENT = 0.05
SAVINGS_RATE = 0.5
INVENTORY_TARGET = 0.2
MONTHLY_INFLATION = 0.000
DIVIDEND_RATE = 0.8
TARGET_FUNDS = 10000

INIT_MACHINERY = 3
INIT_SPEC_MACHINERY = 1

#   Max labour-capital ratios
WORKERS_PER_MACHINE = 5
WORKERS_PER_SPEC_MACHINE = 2

POP_ATTRITION = 0.02
JOB_MOBILITY = 0.02

#   Good types:
#   Commodities: Ore (0), Rare Earths (1), Produce (2), Energy (3), Volatiles (4)
#   Industrial: Electronics (5), Quantronics (6), Alloys (7), Composites (8), Machinery (9), Specialised Machinery (10),
#               Automatons (11), Light Transport (12), Light Ordnance (13), Heavy Transport (14), Heavy Ordnance (15)
#   Commercial: Services (16), Processed Food (17), Consumer Goods (18), Luxury Goods (19)

NUM_GOOD_TYPES = 20

TYPE_ORE = 0
TYPE_RARE_EARTHS = 1
TYPE_PRODUCE = 2
TYPE_ENERGY = 3
TYPE_VOLATILES = 4
TYPE_ELECTRONICS = 5
TYPE_QUANTRONICS = 6
TYPE_ALLOYS = 7
TYPE_COMPOSITES = 8
TYPE_MACHINERY = 9
TYPE_SPECIALISED_MACHINERY = 10
TYPE_AUTOMATONS = 11
TYPE_LIGHT_TRANSPORT = 12
TYPE_LIGHT_ORDNANCE = 13
TYPE_HEAVY_TRANSPORT = 14
TYPE_HEAVY_ORDNANCE = 15
TYPE_SERVICES = 16
TYPE_PROCESSED_FOOD = 17
TYPE_CONSUMER_GOODS = 18
TYPE_LUXURY_GOODS = 19

DICT_GOOD_NAMES = {
    TYPE_ORE: "Ore",
    TYPE_RARE_EARTHS: "Rare Earths",
    TYPE_PRODUCE: "Produce",
    TYPE_ENERGY: "Energy",
    TYPE_VOLATILES: "Volatiles",
    TYPE_ELECTRONICS: "Electronics",
    TYPE_QUANTRONICS: "Quantronics",
    TYPE_ALLOYS: "Alloys",
    TYPE_COMPOSITES: "Composites",
    TYPE_MACHINERY: "Machinery",
    TYPE_SPECIALISED_MACHINERY: "Specialised Machinery",
    TYPE_AUTOMATONS: "Automatons",
    TYPE_LIGHT_TRANSPORT: "Light Transport",
    TYPE_LIGHT_ORDNANCE: "Light Ordnance",
    TYPE_HEAVY_TRANSPORT: "Heavy Transport",
    TYPE_HEAVY_ORDNANCE: "Heavy Ordnance",
    TYPE_SERVICES: "Services",
    TYPE_PROCESSED_FOOD: "Processed Food",
    TYPE_CONSUMER_GOODS: "Consumer Goods",
    TYPE_LUXURY_GOODS: "Luxury Goods"
}

#   Cost of various goods in terms of productivity points
GOOD_COST = [0.2, 0.2, 0.2, 0.2, 0.2, 
             1.0, 5.0, 1.0, 1.0, 2.0, 
             5.0, 5.0, 5.0, 5.0, 10.0, 
             10.0, 0.5, 1.0, 5.0, 10.0]

INIT_PRICE = [0.4, 0.4, 0.4, 0.4, 0.4, 
             1.0, 5.0, 1.0, 1.0, 2.0, 
             5.0, 5.0, 5.0, 5.0, 10.0, 
             10.0, 0.5, 1.0, 5.0, 10.0]

INIT_FIRMS = [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


#   Job types:
#   Upper: Magnate (0)
#   Middle: Administrator (1), Technologist (2)
#   Lower: Labourer (3), Operator (4), Soldier (5), Clerk (6)

NUM_JOB_TYPES = 7

JOB_MAGNATE = 0
JOB_ADMINISTRATOR = 1
JOB_TECHNOLOGIST = 2
JOB_LABOURER = 3
JOB_OPERATOR = 4
JOB_SOLDIER = 5
JOB_CLERK = 6

DICT_JOB_TITLES = {
    JOB_MAGNATE: "Magnate",
    JOB_ADMINISTRATOR: "Administrator",
    JOB_TECHNOLOGIST: "Technologist",
    JOB_LABOURER: "Labourer",
    JOB_OPERATOR: "Operator",
    JOB_SOLDIER: "Soldier",
    JOB_CLERK: "Clerk"
}

MAGNATE_EDUCATION = 6
TECH_EDUCATION = 8
ADMIN_EDUCATION = 6

# INIT_POPULATION = [12, 22, 40, 450, 0, 0, 0]
INIT_POPULATION = [5, 5, 5, 28, 0, 0, 0]
INIT_WAGES = [5.4, 4.27, 3, 1, 1, 1, 1]
INIT_PRODUCTIVITY = [10.0, 0.5, 5.0, 2.0, 2.0, 0.0, 2.0]