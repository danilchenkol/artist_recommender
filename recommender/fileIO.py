'''
Created on 20.07.2013
@author: Marius Kaminskas

contains utility methods to read/write files
'''

import csv
import json

def readCSVFile(filename):
    data = []
    with open(filename, 'rb') as csvfile:
        fileContent = csv.reader(csvfile, doublequote=False, escapechar = "\\")
        next(fileContent)
        for row in fileContent:
            data.append(row)
    return data

def getCSVRowsByFieldValue(filename, fieldName, fieldValue):
    matchingRows = []
    with open(filename, 'rb') as csvfile:
        fileContent = csv.reader(csvfile, doublequote=False, escapechar = "\\")
        fieldNames = next(fileContent)
        fieldIndex = fieldNames.index(fieldName)
        for row in fileContent:
            if (row[fieldIndex] == fieldValue):
                matchingRows.append(row)
    return matchingRows

def getArtistByName(artistName):
    matchingId = 0
    with open('outputData/artist_info.csv', 'rb') as csvfile:
        fileContent = csv.reader(csvfile, doublequote=False, escapechar = "\\")
        next(fileContent)
        for row in fileContent:
            if (json.loads(row[1])['artistName'] == artistName):
                matchingId = row[0]
    return matchingId

def writeCSVFile(filename, fieldList, data):
    with open(filename, 'wb') as csvfile:
        writer = csv.writer(csvfile, doublequote=False, escapechar = "\\")
        writer.writerow(fieldList)
        for row in data:
            writer.writerow(row)
    
    