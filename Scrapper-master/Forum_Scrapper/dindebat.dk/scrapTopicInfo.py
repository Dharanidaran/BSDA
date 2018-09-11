# scrapTopicInfo.py


from bs4 import BeautifulSoup as bs
import requests
import csv
import os
import re
import time



# home_url = "http://www.dindebat.dk/forum/53-tr%C3%A6ning-motion/"



# class ForumLinkInfo:
# 	def __init__(self):
# 		self.homeUrl = "http://www.dindebat.dk/forum/53-træning-motion/"
# 		self.pageCount = 128
# 		self.pageUrl = []
# 		self.topic_details_list = []
# 		self.delimiter = ";"

# 		self.generatePageLinks(self.pageCount)
# 	def generatePageLinks(self, pageCount):
# 		fieldnames = ["Topic_title","Topic_type","Topic_link","Author_name","Author_Url","Link_id","Created_date","Last_posted","Fetch_status","Post_count","Post_views"] #Convert dict keys to list
# 		filename = "Discussion.csv"
# 		fp =  open(filename,'w')
# 		csvwriter = csv.DictWriter(fp,fieldnames = fieldnames,delimiter = self.delimiter)                   
# 		csvwriter.writeheader()
# 		for pageNo in range(1,pageCount):
# 			url = self.homeUrl+"?page=%s"%pageNo
# 			print(url)

# forumObj = ForumLinkInfo()


url = "http://www.dindebat.dk/forum/53-træning-motion/"




def getLinkInfo(url):
	r = requests.get(url)
	html_code =  r.text
	soup = bs(html_code,'html.parser')
	rowgoup_ul = soup.find("ol",class_="ipsDataList")
	list_elms = rowgoup_ul.findChildren("li",class_="ipsDataItem")
	for elm in list_elms:
		Topic_title = ""
		Topic_link = None
		No_of_pages = 1
		Start_datetime = None
		Author_name = ""
		Reply_count = None
		a_tag = elm.find("a",{"data-ipshover":""})
		try:
			if a_tag.text: #If text exists we will proceed if not it will throw and error
				Topic_title = a_tag.get("title").replace(";","").replace("\t"," ").replace("\n","")
				Topic_link = a_tag.get("href").replace("\n","")
				# print(topic_title,topic_link)
				pagination_ul = elm.find("ul",{"class":"ipsPagination"})
				if pagination_ul:
					pagination_li = pagination_ul.find_all("li")
					No_of_pages = pagination_li[-1].text
				
				metaElem = elm.find("div",{"class":"ipsDataItem_meta"})
				if metaElem:
					Author_name = metaElem.find("span").text.split(",")[0].replace("af ","").replace(";","").replace("\t"," ").replace("\n","")
					Start_datetime = metaElem.find("time").get("title")
				Reply_count = elm.find("span",{"class":"ipsDataItem_stats_number"}).text
				print("%s;%s;%s;%s;%s;%s"%(Author_name, Topic_title, No_of_pages, Start_datetime, Reply_count,Topic_link))
				# print(Topic_link)
			else:
				raise Exception()
		except:
			pass

	time.sleep(0.25)


No_of_pages = 128


for i in range(No_of_pages):
	urlWithQuery =  url+"?page=%s"%(i)
	

	getLinkInfo(urlWithQuery)




