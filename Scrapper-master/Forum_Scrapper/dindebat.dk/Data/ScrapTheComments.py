# ScrapTheComments.py


from bs4 import BeautifulSoup as bs
import requests
import csv
import os
import re

import time

filepath = os.getcwd()+"/"+"LinkInfo2.csv"
writepath = os.getcwd()+"PostExtracted.csv"
fieldnames = ["Count","Topic_link","Post","Author","AuthorReputation","AuthorPostCount" ] 


fp = open(filepath)
csvReader = csv.reader(fp,delimiter=";")
fieldnames = ["counter","source_url","datetime","author_name","author_rep","comment","comment_reply" ] 
fw =  open(writepath,'w')
dictWriter = csv.DictWriter(fw,fieldnames=fieldnames,delimiter=";")


def requestPage(url):
	r = requests.get(url)
	if r.status_code == 200:
		return r
	else:
		return None

# url_to_scrap = "http://www.dindebat.dk/topic/708589-l%C3%B8bet%C3%B8j-til-efter%C3%A5rvinter/"
# url_to_scrap = "http://www.dindebat.dk/topic/606307-de-s%C3%A6reste-oplevelser-i-fitnesscenteret/"
# r = requestPage(url_to_scrap)
# soupObj =  bs(r.text,'html.parser')




def scrapPostDetails(soupObj,counter,url_to_scrap):
	postInfoList = []
	#Get the article or post element into one array
	all_posts_in_a_page = soupObj.find_all("article",{"class":"cPost"})
	comment = None #Variable to store the comment
	comment_reply = None
	# print(len(all_posts_in_a_page))
	# try:
	#Iterate throw single post at a time to get the information
	for cPost in all_posts_in_a_page:
		postInfoDict = {}
		comment = None
		comment_reply = None
		cPost_contentWrap = cPost.find("div",{"class","ipsContained"})
		#Check if there is blockquote (comment)
		blockquote = cPost_contentWrap.find("blockquote","ipsQuote")
		if blockquote != None:
			#So we have a comment to store
			comment = blockquote.text.replace("\t","").replace("\n","")
			comment_reply =""
			#loop though para tags to get the replies
			p_list = cPost_contentWrap.findChildren("p")
			counter=0
			for para in p_list:
				if counter == 0 or para.parent.name=="blockquote":
					counter = counter +1
					continue
				comment_reply = comment_reply +para.text
				comment_reply = comment_reply.replace("\t","").replace("\n","")
		if comment == None:
			comment = ""
			ipsContained = cPost.find("div",{"class","ipsContained"})
			comment = ipsContained.text.replace("\t","").replace("\n","")
		#Get Author Meta
		try:
			datetime = cPost.find("time").replace("\t","").replace("\n","")
		except:
			datetime = None
		try:
			author_name = cPost.find("h3",{"class","cAuthorPane_author"}).find("span",{"style":"color:#"}).text.replace("\t","").replace("\n","")
		except:
			author_name= None

		try:
			author_rep = cPost.find("span",{"class","ipsRepBadge"}).text.replace("\t","").replace("\n","").replace(" ","")
		except:
			author_rep = None


		postInfoDict["author_name"] = author_name
		postInfoDict["author_rep"] = author_rep
		postInfoDict["datetime"] = datetime
		postInfoDict["comment"] = comment
		postInfoDict["comment_reply"] = comment_reply
		postInfoDict["counter"] = counter
		postInfoDict["source_url"]=url_to_scrap

		postInfoList.append(postInfoDict)
	# except:
		# print("Page Formating Error")
	return postInfoList

counter = 1
errorCount = 0
totalLinkCount = 3201
start_time = time.time()
dictWriter.writeheader()

#Skip the header 
next(csvReader)

for row in csvReader:
	page_time = time.time()
	rowList = []
	url_to_scrap = row[5]
	r = requestPage(url_to_scrap)
	pagePosts = []
	#check if the request is successfull
	if r!=None:
		soupObj =bs(r.text,'html.parser')
		pagePosts = scrapPostDetails(soupObj,counter,url_to_scrap)
		for item in pagePosts:
			dictWriter.writerow(item)
	else:
		print("Error Link", url_to_scrap)
		errorCount += 1
	print(("Fetching in progress, completed %s")%(counter/totalLinkCount))
	print(("Took %s seconds to process %s")%(time.time()- page_time, url_to_scrap))

	counter += 1

print("Took %s seconds to finish the process" %(time.time()- start_time))


# scrapPostDetails(soupObj)