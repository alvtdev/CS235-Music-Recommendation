import sys
import os
import pprint
import json

trainFile = ""
testFile= ""

#list of indices in train/test sets for characteristics
acousticness = 3
danceability = 4
energy = 5
instrumentalness = 6
liveness = 7
speechiness = 8

def readFiles(filename):
    F = open(filename, "r")
    datatable = []
    for line in F:
        data = line.split("\t")
        data = data[0:-1]
        datatable.append(data)
    return datatable

def getSubset(fullSet, index):
    subSet = [fullSet[index] for item in fullSet]
    return subSet

def calcStats(subSet):
    #TODO: calculate mean/median/standard deviation of a set of audio features
    return

def genMusicList(testSet):
    #TODO: iterate through testSet, comparing audio feature values to 
    #calculated statistics, recommend if within 1 std. dev.
    return=

def main():
    if len(sys.argv) > 2:
        trainFile = sys.argv[1]
        testFile = sys.argv[2]
    else:
        print "Proper use: python suggestSongs.py <trainingSetFile> <testSetFile>"
        print "(both trainingSetFile and testSetFile must be .tsv)"
        sys.exit()

    print "trainFile = " + trainFile + "\n testFile = " + testFile
    pp = pprint.PrettyPrinter(depth=6)
    trainSet = readFiles(trainFile)
    testSet = readFiles(testFile)
    #pp.pprint(trainSet)
    #pp.pprint(testSet)



if __name__ == "__main__":
    main()
