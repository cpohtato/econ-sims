#   Simple market simulation - no buy/sell orders
#   1. Producers add goods to inventory
#   2. Consumers buy goods, giving firms money

from xml.etree.ElementTree import PI
import matplotlib.pyplot as plt
import numpy as np
import random

SIM_LENGTH = 100

numFirms = 1000
firmInv = 2000
firmInvTarget = 2000
firmOrder = 1

numConsumers = 1000
consumerDemand = 1.0

accumError = 0

arrProduced = np.zeros(SIM_LENGTH)
arrConsumed = np.zeros(SIM_LENGTH)
arrInventory = np.zeros(SIM_LENGTH)
arrTime = range(SIM_LENGTH)

for step in range(SIM_LENGTH):
    aggProduced = numFirms * firmOrder
    firmInv += aggProduced
    arrProduced[step] = aggProduced

    #consumerDemand = 1.0 + 0.5 * np.sin(step/(2*np.pi))

    consumerDemand = 1 + random.gauss(0,0.1)
    if (consumerDemand < 0):
        consumerDemand = 0

    aggDemanded = numConsumers * consumerDemand

    if (aggDemanded < firmInv):
        firmInv -= aggDemanded
        arrConsumed[step] = aggDemanded
    else:
        arrConsumed[step] = firmInv
        firmInv = 0

    arrInventory[step] = firmInv

    surplus = firmInvTarget - firmInv
    firmOrder = ((surplus/abs(surplus)) * (abs(surplus))**1.01 + aggDemanded) / numFirms

plt.plot(arrTime, arrProduced, label='Produced')
plt.plot(arrTime, arrConsumed, label='Consumed')
plt.plot(arrTime, arrInventory, label='Inventory')
plt.legend()
plt.show()