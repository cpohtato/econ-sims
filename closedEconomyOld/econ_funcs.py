from econ_const import *
import math

def findBaseLabourDemands(goodType):

    #   Each firm should employ 50 demos per size level

    baseLabourDemands = [0] * NUM_JOB_TYPES

    #   Commodity industries - low tech, labour intensive
    if ((goodType == TYPE_ORE) or (goodType == TYPE_RARE_EARTHS) or (goodType  == TYPE_PRODUCE) or 
        (goodType == TYPE_ENERGY) or (goodType == TYPE_VOLATILES)):

        baseLabourDemands[JOB_MAGNATE] = 1
        baseLabourDemands[JOB_ADMINISTRATOR] = 2
        baseLabourDemands[JOB_TECHNOLOGIST] = 2
        baseLabourDemands[JOB_LABOURER] = 45

    #   Electronics, refining, industrial, food processing, manufacturing - mature technology
    elif ((goodType == TYPE_ELECTRONICS) or (goodType == TYPE_ALLOYS) or (goodType == TYPE_COMPOSITES) or 
        (goodType == TYPE_MACHINERY) or (goodType == TYPE_LIGHT_TRANSPORT) or (goodType == TYPE_LIGHT_ORDNANCE) or
        (goodType == TYPE_HEAVY_TRANSPORT) or (goodType == TYPE_HEAVY_ORDNANCE) or 
        (goodType == TYPE_PROCESSED_FOOD) or (goodType == TYPE_CONSUMER_GOODS)):

        baseLabourDemands[JOB_MAGNATE] = 1
        baseLabourDemands[JOB_ADMINISTRATOR] = 4
        baseLabourDemands[JOB_TECHNOLOGIST] = 10
        baseLabourDemands[JOB_OPERATOR] = 35

    #   Quantronics, specialised machinery and automatons - advanced technology
    elif ((goodType == TYPE_QUANTRONICS) or (goodType == TYPE_SPECIALISED_MACHINERY) or (goodType == TYPE_AUTOMATONS)):
        baseLabourDemands[JOB_MAGNATE] = 1
        baseLabourDemands[JOB_ADMINISTRATOR] = 4
        baseLabourDemands[JOB_TECHNOLOGIST] = 35
        baseLabourDemands[JOB_OPERATOR] = 10

    #   Services - financial, legal, admin, etc.
    elif (goodType == TYPE_SERVICES):
        baseLabourDemands[JOB_MAGNATE] = 1
        baseLabourDemands[JOB_ADMINISTRATOR] = 9
        baseLabourDemands[JOB_CLERK] = 40

    #   Luxury goods - difficult to make
    elif (goodType == TYPE_LUXURY_GOODS):
        baseLabourDemands[JOB_MAGNATE] = 1
        baseLabourDemands[JOB_ADMINISTRATOR] = 9
        baseLabourDemands[JOB_TECHNOLOGIST] = 20
        baseLabourDemands[JOB_OPERATOR] = 20

    return baseLabourDemands

def wipeLogs():
    with open("closedEconomyOld/log/labourOrders.txt", "w") as logFile:
        logFile.write("")
        
    with open("closedEconomyOld/log/sellOrders.txt", "w") as logFile:
        logFile.write("")
