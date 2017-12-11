import sys
import os
import pprint
import json
import math

trainFile = ""
testFile= ""

#indices in train/test sets for features
acousticness = 3
danceability = 4
energy = 5
instrumentalness = 6
liveness = 7
speechiness = 8

#individual sets for each feature
A = []
D = []
E = []
I = []
L = []
S = []

#stats for each feature
# index 0 = mean
# index 1 = std. dev
Astats = []
Dstats = []
Estats = []
Istats = []
Lstats = []
Sstats = []
allStats = []

def readFiles(filename):
    F = open(filename, "r")
    datatable = []
    for line in F:
        data = line.split("\t")
        data[-1] = data[-1].strip()
        datatable.append(data)
    return datatable

def getSubset(fullSet, index):
    subSet = []
    for row in fullSet[1:]:
        print row[index]
        subSet.append(row[index])
    #print subSet
    return subSet

def populateSubsets(trainSet, alpha = 1):
    for row in trainSet[1:]:
        A.append(float(row[acousticness]))
        D.append(float(row[danceability]))
        E.append(float(row[energy]))
        I.append(float(row[instrumentalness]))
        L.append(float(row[liveness]))
        S.append(float(row[speechiness]))
    Astats = calcStats(A, alpha)
    Dstats = calcStats(D, alpha)
    Estats = calcStats(E, alpha)
    Istats = calcStats(I, alpha)
    Lstats = calcStats(L, alpha)
    Sstats = calcStats(S, alpha)
    return [Astats, Dstats, Estats, Istats, Lstats, Sstats]

#calculate mean and std. dev. from feature statistics
def calcStats(subSet, alpha = 1):
    #calculate mean
    mean = sum(subSet)/len(subSet)
    #calculate standard deviation
    diff = []
    for i in subSet:
        diff.append(pow(i-mean, 2))
    sumdiff = sum(diff)
    stdev = math.sqrt( sumdiff / len(subSet) )
    #stats = [mean, stdev]
    #calculate lower and upper bounds
    lb = mean - alpha*stdev
    ub = mean + alpha*stdev
    stats = [lb, ub]
    return stats

#function to get list of existing genres from training data
def getGenres(trainSet):
    genreList = []
    for row in trainSet[1:]:
        gList = row[2].split(",")
        for genre in gList:
            if not genre in genreList:
                genreList.append(genre)
    return genreList

#function to check if at least 1 genre classification exists
def checkGenre(testGenres, genreList):
    result = False
    for genre in testGenres:
        if genre in genreList:
            result = True
    return result

#check value of stats to see if they're within range (calculated by calcStats)
#return true if more than half of the stats are in range (default=1 std. dev.)
def checkStats(tsRow, allStats):
    statCount = 0
    for i in range(0, len(tsRow)):
        #print str(i) + "-" + str(tsRow[i]) + " - ",
        #print str(allStats[i][0]) + " - " + str(allStats[i][1])
        if allStats[i][0] < float(tsRow[i]) < allStats[i][1]:
            statCount += 1

    if statCount >= 3:
        return True
    else:
        return False

def genMusicList(testSet, allStats, genreList):
    #TODO: iterate through testSet, comparing audio feature values to 
    #calculated statistics, recommend if within 1 std. dev.
    for row in testSet[1:]:
        testGenres = row[2].split(",")
        tsRow = row[3:]
        if checkGenre(testGenres, genreList) and checkStats(tsRow, allStats):
            print row[0] + " - " + row[1]
    return

def main():
    alpha = 0.0
    if len(sys.argv) > 3:
        trainFile = sys.argv[1]
        testFile = sys.argv[2]
        alpha = sys.argv[3]
    elif len(sys.argv) > 2:
        trainFile = sys.argv[1]
        testFile = sys.argv[2]
        alpha = 0.5
    else:
        print "Proper use: python suggestSongs.py <trainingSetFile> <testSetFile>"
        print "(both trainingSetFile and testSetFile must be .tsv)"
        sys.exit()

    #print "trainFile = " + trainFile + "\n testFile = " + testFile
    pp = pprint.PrettyPrinter(depth=6)
    trainSet = readFiles(trainFile)
    testSet = readFiles(testFile)
    allStats = populateSubsets(trainSet, alpha)
    genreList = getGenres(trainSet)
    genMusicList(testSet, allStats, genreList)


if __name__ == "__main__":
    main()
