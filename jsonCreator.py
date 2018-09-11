# jsonCreator.py

import os
import csv
import json 


filepath = os.path.join(os.getcwd(),'Data','sample.csv')
fileObj = open(filepath)
fieldnames = ["PostDbId","DbId","ParentDbId","Fbid","CreatedDate","ActorId","ActorName","ActionType","PostType","LikeCount","ShareCount","TextValue"]

writepath = os.path.join(os.getcwd(),'Data','sampleOutput.csv')
writeObj = open(writepath,'w')

csvreader = csv.DictReader(fileObj,fieldnames=fieldnames,delimiter=";")

counter = 0
fileList = []
for rowDict in csvreader:
	if counter ==0 :
		counter =1
		continue
	fileList.append(rowDict)

(json.dump(fileList,writeObj, sort_keys=True, indent=4))

