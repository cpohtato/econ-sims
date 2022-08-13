import numpy as np
import random

WAGE_VISCOSITY = 0.2
PRICE_VISCOSITY = 0.2
SURPLUS_CONST = 0.3

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
GOOD_COST = [0.5, 0.5, 0.5, 0.5, 0.5, 
             1.0, 5.0, 1.0, 1.0, 2.0, 
             5.0, 5.0, 5.0, 5.0, 10.0, 
             10.0, 0.5, 1.0, 5.0, 10.0]

INIT_PRICE = [0.2, 0.2, 0.2, 0.2, 0.2, 
             1.0, 5.0, 1.0, 1.0, 2.0, 
             5.0, 5.0, 5.0, 5.0, 10.0, 
             10.0, 0.5, 1.0, 5.0, 10.0]

INIT_FIRMS = [0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


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

INIT_POPULATION = [6, 15, 15, 400, 0, 0, 0]
INIT_WAGES = [10, 5, 5, 2, 2, 2, 2]