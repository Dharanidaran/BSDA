# RemoveDuplicates.py
import requests
import re
import time
import csv
import os




ListID = []

filepath =  os.getcwd()+"/TopicStore/Discussion.csv"
fp =  open(filepath)
csvReader =  csv.reader(fp,delimiter=";")
next(csvReader)

for row in csvReader:
	ListID.append(row[5])



# print(len(ListID))

TopicIdSet = set(ListID)

fp.close()



#Close and reopen the file again
fp =  open(filepath)
csvReader =  csv.reader(fp,delimiter=";")


filepathToWrite = os.getcwd()+"/TopicStore/NonDuplicate.csv"
fw = open(filepathToWrite,'w')






csvWriter = csv.writer(fw,delimiter=";")



for row in csvReader:
	if row[5] in TopicIdSet:
		TopicIdSet.remove(row[5])
		print(len(TopicIdSet))
		csvWriter.writerow(row)
	else:
		pass