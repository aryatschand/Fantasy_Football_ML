# Created By Arya Tschand 6/27/2020

# Import libraries for csv read, data visualization, and linear regression
import csv
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

# Parse CSV files to extract player statistics
def parseCSV(fileName):
    returnArray = []

    # Open and read file with filename parameter
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        # Read each non-header row
        for row in csv_reader:
            if line_count != 0:

                # If the player is a running back, trim out unwanted characters and save to a return array
                if row[4].lower() == "rb":
                    tempArr = []
                    for x in row:
                        if "\\" in x :
                            tempArr.append(x.split('\\')[0].replace("*", "").replace("+", ""))
                        else :
                            tempArr.append(x)
                    returnArray.append(tempArr)
            line_count+=1
    return returnArray

# Get rushing and receiving data for 2017, 2018, 2019
receiving2017 = parseCSV('2017receiving.csv')
rushing2017 = parseCSV('2017rushing.csv')
receiving2018 = parseCSV('2018receiving.csv')
rushing2018 = parseCSV('2018rushing.csv')
receiving2019 = parseCSV('2019receiving.csv')
rushing2019 = parseCSV('2019rushing.csv')

nameList = []

# Search for players that have significant data in 2017, 2018, and 2019
for x in range(0, len(rushing2017)):
    for y in range(0, len(rushing2018)):
        for z in range(0, len(rushing2019)):

            # If the player is in all rushing datasets, save the indexes of player statistics
            if rushing2017[x][1] == rushing2018[y][1] and rushing2018[y][1] == rushing2019[z][1]:
                addArr = []
                addArr.append(rushing2017[x][1])
                addArr.append(x)
                addArr.append(y)
                aIndex = -1
                bIndex = -1
                cIndex = -1

                # If the player has significant receiving stats, save it. If not, ignore it
                for a in range(0, len(receiving2017)):
                    if receiving2017[a][1] == rushing2017[x][1]:
                        aIndex = a
                for b in range(0, len(receiving2018)):
                    if receiving2018[b][1] == rushing2017[x][1]:
                        bIndex = b
                for c in range(0, len(receiving2019)):
                    if receiving2019[c][1] == rushing2017[x][1]:
                        cIndex = c
                addArr.append(aIndex)
                addArr.append(bIndex)
                addArr.append(z)
                addArr.append(cIndex)
                nameList.append(addArr)

# Based on the player statistic indexes, calculate the fantase points for each year
def getPoints(details):
    pointsA = 0.0
    pointsB = 0.0
    pointsC = 0.0

    # Grab player rushing statistics for each year 
    rushingA = rushing2017[details[1]]
    rushingB = rushing2018[details[2]]
    rushingC = rushing2019[details[5]]

    # Calculate fantasy points from rushing
    pointsA = float(float(rushingA[8])/10.0 + float(rushingA[9])*6 - float(rushingA[14])*2)
    pointsB = float(float(rushingB[8])/10.0 + float(rushingB[9])*6 - float(rushingB[14])*2)
    pointsC = float(float(rushingC[8])/10.0 + float(rushingC[9])*6 - float(rushingC[14])*2)

    # If the player has significant receiving stats, take it into account
    if details[3] != -1 and details[4] != -1 and details[6] != -1:
        
        # Grab player receiving statistics for each year
        receivingA = receiving2017[details[3]]
        receivingB = receiving2018[details[4]]
        receivingC = receiving2019[details[6]]

        # Calculate fantasy points for receiving and add it to total
        pointsA += float(float(receivingA[8])/2.0 + float(receivingA[10])/10.0 + float(receivingA[12])*6)
        pointsB += float(float(receivingB[8])/2.0 + float(receivingB[10])/10.0 + float(receivingB[12])*6)
        pointsC += float(float(receivingC[8])/2.0 + float(receivingC[10])/10.0 + float(receivingC[12])*6)
    
    return int(pointsA), int(pointsB), int(pointsC)

# Get a specific player statistic for desired year
def getStat(rush, details, column):
    
    # Look into desired data set (rushing or receiving)
    if rush == 1:

        # Grab specific rushing statistic and calculate change between years
        a = float(rushing2017[details[1]][column])
        b = float(rushing2018[details[2]][column])
        c = float(rushing2019[details[5]][column])
        change1 = b-a
        change2 = c-b
        return a, b, change1, c, change2
    else:

        # Grab specific receiving statistic and calculate change between years
        a = float(receiving2017[details[3]][column].replace("%", ""))
        b = float(receiving2018[details[4]][column].replace("%", ""))
        c = float(receiving2019[details[6]][column].replace("%", ""))
        change1 = b-a
        change2 = c-b
        return a, b, change1, c, change2

DataList = []

# Iterate through each player to create a full data list with desired statistics
for x in nameList:
    PlayerData = []
    PlayerData.append(x[0])
    A = []
    Change = []
    B = []
    Change2 = []
    C = []

    # Get fantasy points for each year as well as change between years
    pointsA, pointsB, pointsC = getPoints(x)
    pointsChange = pointsB-pointsA
    pointsChange2 = pointsC-pointsB
    PlayerData.append(pointsC)

    # Find number of games played - most stats are done on a per game basis to neglect injury
    gamesA = float(rushing2017[x[1]][5])
    gamesB = float(rushing2018[x[2]][5])
    gamesC = float(rushing2019[x[5]][5])

    A.append(pointsA)
    Change.append(pointsChange)
    B.append(pointsB)
    Change2.append(pointsChange2)
    C.append(pointsC)

    # Location of desired stats in datasets
    statTypeArr = [1,1,1,0,0,0,0,1,1,0,0]
    columnArr = [7,8,9,7,8,10,12,14,12,11,9]

    # Iterate through each statistic and store value
    for y in range(0, len(statTypeArr)):
        a,b,c1,c,c2 = getStat(statTypeArr[y], x, columnArr[y])

        # If statistic should be per game or as is
        if y < 8:
            A.append(round(a/gamesA, 4))
            B.append(round(b/gamesB, 4))
            Change.append(round((b/gamesB)-(a/gamesA), 4))
            C.append(round(c/gamesC, 4))
            Change2.append(round((c/gamesC)-(b/gamesB), 4))
        else:
            A.append(round(a, 4))
            B.append(round(b, 4))
            Change.append(round(c1, 4))
            C.append(round(c, 4))
            Change2.append(round(c2, 4))
    
    # Append data to full data list
    PlayerData.append(A)
    PlayerData.append(Change)
    PlayerData.append(B)
    PlayerData.append(Change2)
    PlayerData.append(C)
    DataList.append(PlayerData)

xArr = []
yArr = []
SignificanceArray = []

# Global function to get the significance of each statistic
def getSignificance():

    # Iterate through each statistic for each year
    for year in range(0, 3):
        for stat in range(0, 12):
            xArr = []
            yArr = []

            # Populate an X (unique statistic) and Y (fantasy points) list for regression
            for player in DataList:
                if player[year+2][stat] != 0:
                    xArr.append(player[year+2][stat])
                    yArr.append(player[1])

            # Store the data as a numpy array and reshape for regression
            x = np.array(xArr).reshape((-1, 1))
            y = np.array(yArr)

            # Regress the XY data and store the slope and intercept
            model = LinearRegression()
            model.fit(x, y)
            intercept = model.intercept_
            slope = model.coef_[0]

            # Calculate the overall error for each regression function to find accuracy
            error = 0
            for x in range(0, len(xArr)):

                # Access the real value and calculate the predicted value
                real = yArr[x]
                predict = xArr[x] * slope + intercept

                # Find the absolute value of the difference and append to the overall error
                tempError = abs(real-predict)
                error += tempError

            # Find the error per point
            error /= len(xArr)

            # Normalize the slopes based on the magnitude of the X values
            slope /= (max(yArr)/max(xArr))

            # Calculate the significance of the correlation between statistic and fantasy success and store
            significance = (100-error)/100.0 * slope
            SignificanceArray.append([year,stat,significance])
    return SignificanceArray
