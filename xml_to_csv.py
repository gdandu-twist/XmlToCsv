import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv

def average(arr1):
    return sum(arr1) / len(arr1)

def appEmpty(arr2):
    for j in range(2,385):
        arr2.append('')
    return arr2


#initialize variables
wellName = ["Well Position"]
dataList = ["Read value"]
aveArr = ["Average"]
incArr = ["Incubation Time"]
tempArr = []
plateData = []
alpha = 'A'
x = 1
#thresholdCSV = "IncubationTimeThresholds.csv"

#read in xml file 
xmlFile = input("Enter Plate Data File Name: ")
xmlFilePath = "C:\\Users\\gdandu\\Desktop\\Python Projects\\"
xmlFilePath = xmlFilePath + xmlFile
#print(xmlFilePath)
xmlparse = ET.parse(xmlFilePath)
#xmlparse = ET.parse(r'C:\Users\gdandu\Desktop\Python Projects\Target Plate_1.xml')
root = xmlparse.getroot()

#get plate title to name output file 
for plate in root.iter("PlateSection"):
    plateName = plate.get('Name')
    #print(plateName)
outputFileName = plateName + "_Data.csv"
outputPlateData = plateName + "_Plate_Data.csv"

#make array of well numbers
for well in root.iter('Well'):
    #wellNum = well.get('Name')
    wellName.append(well.get('Name'))  

#make array of raw data values
for data in root.iter('RawData'): 
    dataList.append(data.text)

#tempArr = np.copy(dataList)
#tempArr.pop(0)
#tempArr = list(map(float, tempArr))
#ave = average(tempArr)
#aveArr.append(ave)
#print(dataList)

#calculate average and build average array 
dataCopy = np.copy(dataList)
dataList.pop(0)
dataList = list(map(float, dataList))
ave = average(dataList)
aveArr.append(ave)
aveArrCopy = np.copy(aveArr)
aveArr = appEmpty(aveArr)

#print(aveArr)
#print(tempArr)

#get incubation time corresponding to calculated average and build incubation time array 
with open('IncubationTimeThresholds.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 1
    next(csv_reader)
    #print(ave)
    for row in csv_reader:
        #print(float(row[0]),float(row[1]))
        if float(row[0]) < ave and ave < float(row[1]):
            #print('entering if')
            incTime = row[2]
            incArr.append(incTime)
            break
incArrCopy = np.copy(incArr)
incArr = appEmpty(incArr)

#create raw data csv
with open(outputFileName, 'w', newline='') as csvfile:
    dataWriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    result_array = zip(wellName, dataCopy, aveArr, incArr)
    aveArr = zip(aveArr)
    dataWriter.writerows(result_array)
    dataWriter.writerows("\n")
    #print(result_array)
    #dataWriter.writerows(aveArr)

#create 384 plate milti-D array 
tempArr = [""]
for numCounter in range(1,25):
    tempArr.append(numCounter)   
plateData.append(tempArr)

for alphaCounter in range(0,16):
    tempArr = []
    tempArr.append(chr(ord(alpha) + alphaCounter))
    #print(tempArr)
    for dataCounter in range(x,x+24):
        tempArr.append(dataCopy[dataCounter])
        #print(tempArr)
    plateData.append(tempArr)
    x = x+24
plateData.append(aveArrCopy)
plateData.append(incArrCopy)

#print(tempArr)
#print(plateData)

#create raw data plate map csv
with open(outputPlateData, 'w', newline='') as csvfile:
    dataWriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
    dataWriter.writerows(plateData)
