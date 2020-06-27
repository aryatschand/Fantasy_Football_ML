# Created By Arya Tschand 6/27/2020

# Import libraries for csv read, data visualization, and linear regression
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Import Analyze.py file to access SignificanceArray
import Analyze

# Parse CSV files to extract player statistics
def parseCSV(fileName):
    returnArray = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                if row[4].lower() == "rb":
                    tempArr = []
                    for x in row:
                        if "\\" in x :
                            toAdd = x.split('\\')[0].replace("*", "").replace("+", "")
                            if toAdd[len(toAdd)-1] == " ":
                                toAdd = toAdd[0: len(toAdd)-1]
                            tempArr.append(toAdd)
                        else :
                            tempArr.append(x)
                    returnArray.append(tempArr)
            line_count+=1
    return returnArray

# Get rushing and receiving data for 2018 and 2019
receiving2018 = parseCSV('2018receiving.csv')
rushing2018 = parseCSV('2018rushing.csv')
receiving2019 = parseCSV('2019receiving.csv')
rushing2019 = parseCSV('2019rushing.csv')

nameList = []

# Search for players that have significant data in 2018 and 2019
for x in range(0, len(rushing2018)):
    for y in range(0, len(rushing2019)):
        if rushing2018[x][1] == rushing2019[y][1]:
            addArr = []
            addArr.append(rushing2018[x][1])
            addArr.append(x)
            addArr.append(y)
            aIndex = -1
            bIndex = -1
            for a in range(0, len(receiving2018)):
                if receiving2018[a][1] == rushing2018[x][1]:
                    aIndex = a
            for b in range(0, len(receiving2019)):
                if receiving2019[b][1] == rushing2018[x][1]:
                    bIndex = b
            addArr.append(aIndex)
            addArr.append(bIndex)
            nameList.append(addArr)

# Based on the player statistic indexes, calculate the fantase points for each year
def getPoints(details):
    pointsA = 0.0
    pointsB = 0.0

    rushingA = rushing2018[details[1]]
    rushingB = rushing2019[details[2]]

    pointsA = float(float(rushingA[8])/10.0 + float(rushingA[9])*6 - float(rushingA[14])*2)
    pointsB = float(float(rushingB[8])/10.0 + float(rushingB[9])*6 - float(rushingB[14])*2)

    if details[3] != -1 and details[4] != -1:
        receivingA = receiving2018[details[3]]
        receivingB = receiving2019[details[4]]

        pointsA += float(float(receivingA[8])/2.0 + float(receivingA[10])/10.0 + float(receivingA[12])*6)
        pointsB += float(float(receivingB[8])/2.0 + float(receivingB[10])/10.0 + float(receivingB[12])*6)
    
    return int(pointsA), int(pointsB)

# Get a specific player statistic for desired year
def getStat(rush, details, column):
    if rush == 1:
        a = float(rushing2018[details[1]][column])
        b = float(rushing2019[details[2]][column])
        change1 = b-a
        return a, b, change1
    else:
        a = float(receiving2018[details[3]][column].replace("%", ""))
        b = float(receiving2019[details[4]][column].replace("%", ""))
        change1 = b-a
        return a, b, change1

DataList = []

# Iterate through each player to create a full data list with desired statistics
for x in nameList:
    PlayerData = []
    PlayerData.append(x[0])

    A = []
    Change = []
    B = []
    pointsA, pointsB = getPoints(x)
    pointsChange = pointsB-pointsA
    PlayerData.append(0)

    gamesA = float(rushing2018[x[1]][5])
    gamesB = float(rushing2019[x[2]][5])

    A.append(pointsA)
    Change.append(pointsChange)
    B.append(pointsB)

    statTypeArr = [1,1,1,0,0,0,0,1,1,0,0]
    columnArr = [7,8,9,7,8,10,12,14,12,11,9]

    for y in range(0, len(statTypeArr)):
        a,b,c1 = getStat(statTypeArr[y], x, columnArr[y])
        if y < 8:
            A.append(round(a/gamesA, 4))
            B.append(round(b/gamesB, 4))
            Change.append(round((b/gamesB)-(a/gamesA), 4))
        else:
            A.append(round(a, 4))
            B.append(round(b, 4))
            Change.append(round(c1, 4))
    
    PlayerData.append(A)
    PlayerData.append(Change)
    PlayerData.append(B)
    DataList.append(PlayerData)

# Access the SignificanceArray by calling function from Analyze.py
SignificanceArray = Analyze.getSignificance()

success = []

# Calculate the projected success for each player
for player in DataList:
    playerSuccess = 0

    # Iterate through each statistic for each year
    for year in range(0, 3):
        for stat in range(0, 12):

            # Project player success by multiplying player statistic by the calculated significance of that statistic 
            playerSuccess += player[year+2][stat] * SignificanceArray[year*12+stat][2]
    success.append([player[0], playerSuccess])

print(success)