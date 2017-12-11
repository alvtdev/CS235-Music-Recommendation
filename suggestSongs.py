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

def populateSubsets(trainSet):
    for row in trainSet[1:]:
        A.append(float(row[acousticness]))
        D.append(float(row[danceability]))
        E.append(float(row[energy]))
        I.append(float(row[instrumentalness]))
        L.append(float(row[liveness]))
        S.append(float(row[speechiness]))
    Astats = calcStats(A)
    Dstats = calcStats(D)
    Estats = calcStats(E)
    Istats = calcStats(I)
    Lstats = calcStats(L)
    Sstats = calcStats(S)
    return [Astats, Dstats, Estats, Istats, Lstats, Sstats]

def calcStats(subSet):
    #calculate mean
    mean = sum(subSet)/len(subSet)
    diff = []
    for i in subSet:
        diff.append(i-mean)
    sumdiff = sum(diff)
    stdev = math.sqrt( ( math.pow(sumdiff, 2) / len(subSet) ) )
    stats = [mean, stdev]
    return stats

def genMusicList(testSet):
    #TODO: iterate through testSet, comparing audio feature values to 
    #calculated statistics, recommend if within 1 std. dev.
    return

def main():
    if len(sys.argv) > 2:
        trainFile = sys.argv[1]
        testFile = sys.argv[2]
    else:
        print "Proper use: python suggestSongs.py <trainingSetFile> <testSetFile>"
        print "(both trainingSetFile and testSetFile must be .tsv)"
        sys.exit()

    #print "trainFile = " + trainFile + "\n testFile = " + testFile
    pp = pprint.PrettyPrinter(depth=6)
    trainSet = readFiles(trainFile)
    testSet = readFiles(testFile)
    allStats = populateSubsets(trainSet)
    for stat in allStats:
        print stat
    #pp.pprint(trainSet)
    #pp.pprint(testSet)
    #pp.pprint(A)
    #pp.pprint(D)
    #pp.pprint(E)
    #pp.pprint(I)
    #pp.pprint(L)
    #pp.pprint(S)


if __name__ == "__main__":
    main()
