#######################################################
#    Author:      Jacob Laster
#    email:       jlaster
#    ID:          ee364e08
#    Date:        1/16/19
#######################################################

import os
import sys

# Module  level  Variables. (Write  this  statement  verbatim .)
#######################################################
DataPath = os.path.expanduser('~ee364/DataFolder/Prelab02')

def fileList():
    files = [f for f in os.listdir(DataPath) if os.path.isfile(os.path.join(DataPath, f))]
    return files

def getMaxDifference(symbol):
    filename = os.path.join(DataPath, symbol + ".dat")
    with open(filename, "r") as file:
        data = [line.strip().split(',') for line in file.readlines()][2:]
    maxDiff = 0
    maxDate = data[0][0]
    for date in data:
        if float(date[4]) - float(date[5]) > maxDiff:
            maxDiff = float(date[4]) - float(date[5])
            maxDate = date[0]
    return maxDate

def getGainPercent(symbol):
    filename = os.path.join(DataPath, symbol + ".dat")
    with open(filename, "r") as file:
        data = [line.strip().split(',') for line in file.readlines()][2:]
    gain = 0
    for date in data:
        if float(date[1]) > float(date[3]):
            gain += 1
    return 100 * gain / len(data)

if __name__ == "__main__":
    #print(fileList())
    print(getGainPercent("AAPL"))
