from pathlib import Path

f = open("simpleClosedEconomy/econSim-2/names/male.txt", "w")
f.write("")
f.close()

f = open("simpleClosedEconomy/econSim-2/names/female.txt", "w")
f.write("")
f.close()

with open("simpleClosedEconomy/econSim-2/names/yob1880.txt", "r") as file:
    for item in file:
        lineList = item.split(",")
        if (lineList[1] == "M"):
            f = open("simpleClosedEconomy/econSim-2/names/male.txt", "a")
            f.write(lineList[0] + "\n")
            f.close()
        elif (lineList[1] == "F"):
            f = open("simpleClosedEconomy/econSim-2/names/female.txt", "a")
            f.write(lineList[0] + "\n")
            f.close()