# ScrapTheComments.py


from bs4 import BeautifulSoup as bs
import requests
import csv
import os
import re



filepath = os.getcwd()+"/TopicStore/PagesToScrap.csv"
writepath = os.getcwd()+"/TopicStore/PostExtracted2.csv"


fieldnames = [
				"Author_name","Author_post_count","Author_Joined_date","Author_location",
				"Post_text","Signature","Url_to_scrap","Post_type"
				
			] 


fp = open(filepath)
csvReader = csv.reader(fp,delimiter=";")


fw = open(writepath,'w')
dictWriter = csv.DictWriter(fw,fieldnames=fieldnames,delimiter=";")







#Need to parallelize this code in the future
def requestPage(url):
	r = requests.get(url)
	if r.status_code == 200:
		return r
	else:
		return None


def scrapPostDetails(soupObj,url_to_scrap,post_type):
	postInfoList = []
	all_posts_in_a_page = soupObj.find_all("div",{"class":"post"})
	for singlePost in all_posts_in_a_page:
		postInfoDict = {}
		user_info = singlePost.find("div",{"class": "user-info"})
		post_container = singlePost.find("div",{"class": "user-post"})
		try:
			author_name = user_info.find("a").text
			postInfoDict["Author_name"]= author_name.replace(";","")
		except:
			postInfoDict["Author_name"]= None
		try:
			joined_date_text =  user_info.find("span",{"class":"joined_date"}).text
			author_Joined_date  = re.findall('[a-z,A-Z]{3}\s+\d+',joined_date_text)[0]
			postInfoDict["Author_Joined_date"] = author_Joined_date
		except:
			postInfoDict["Author_Joined_date"] = None
		try:
			author_location = user_info.find("span",{"class":"author_location"}).text
			postInfoDict["Author_location"] =  author_location.replace(";","")
		except:
			postInfoDict["Author_location"] =  None
		try:
			post_elements = post_container.findChildren()
			post_text = ""
			for child in post_elements:
			# 	# If the child element has an element which has a class name as 
			# 	# signature we stop looping
				elem_with_class = child.get("class")
				if elem_with_class != None:
					if elem_with_class[0] == "signature":
						break
				post_text  = post_text +" "+child.text
			# 	print("------------")
			postInfoDict["Post_text"] = post_text.replace(";","").replace("\n"," ")
		except:
			post_elements = None
		try:
			sign =  singlePost.find("div",{"class":"signature"})
			signature_text = sign.text
			postInfoDict["Signature"] = signature_text.replace(";","").replace("\n","")
		except:
			postInfoDict["Signature"] = None

		postInfoDict["Url_to_scrap"] = url_to_scrap
		postInfoDict["Post_type"] = post_type
		postInfoList.append(postInfoDict)

	return postInfoList

def scrapOriginalPostDetails(soupObj,author_name,url_to_scrap,post_type):
	# This function is to return a list of dictionary that has 
	original_topic_list = []
	original_topic_info_dict = {}
	original_topic = soupObj.find("div",{"class":"original-topic"})
	post_para_obj = original_topic.find("div",{"class":"user-post"})
	user_info = original_topic.find("div",{"class":"user-info"})
	signature_span_list = []
	post_container = original_topic.find("div",{"class":"user-post"})
	author_post_count = ""
	author_Joined_date = ""
	author_location =""
	try:
		signature_span_list.extent(original_topic.find("div",{"class":"signature"}).find_all("span"))
	except:
		pass
	try:
		author_post_count_text = user_info.find("span",{"class":"post_count"}).text
		author_post_count = re.findall('\d+,?\d+',author_post_count_text)[0]
	except:
		author_post_count = None
	try: 
		author_Joined_date_text = user_info.find("span",{"class":"joined_date"}).text
		author_Joined_date  = re.findall('[a-z,A-Z]{3}\s+\d+',author_Joined_date_text)[0]
	except:
		author_Joined_date = None
	try:
		author_location = user_info.find("span",{"class":"author_location"}).text
	except:
		author_location = None
	signature = ""
	for span in signature_span_list:
		signature = signature + span.text
	post_text = ""
	try:
		post_elements = post_container.findChildren()
		for child in post_elements:
		# 	# If the child element has an element which has a class name as 
		# 	# signature we stop looping
			elem_with_class = child.get("class")
			if elem_with_class != None:
				if elem_with_class[0] == "signature":
					break
			post_text  = post_text +" "+child.text
		# 	print("------------")
		post_text = post_text
	except:
		post_text=""
	original_topic_info_dict["Author_name"] = author_name.replace(";","") #arg
	original_topic_info_dict["Author_post_count"] = author_post_count
	original_topic_info_dict["Author_Joined_date"] =  author_Joined_date
	original_topic_info_dict["Author_location"] = author_location
	original_topic_info_dict["Post_text"] = post_text.replace(";","").replace("\n"," ")
	original_topic_info_dict["Signature"] = signature.replace(";","").replace("\n"," ")
	original_topic_info_dict["Url_to_scrap"] = url_to_scrap #arg
	original_topic_info_dict["Post_type"] = post_type #arg
	original_topic_list.append(original_topic_info_dict)
	return original_topic_list





counter =1
errorCount = 0
dictWriter.writeheader()
TotalCount = 30500


for i in range(6319):
	next(csvReader)
	counter = counter+1






for row in csvReader:
	rowList = []
	urlCount = row[0]
	LinkId = row[1]
	postType = row[2]
	url_to_scrap = row[3]
	ifFirstPage = row[4]
	author_name = row[5]
	r = requestPage(url_to_scrap)
	pagePosts = []
	#Check if the request is successfull:
	if r != None:
		#Create a soup object for the page
		soupObj = bs(r.text,'html.parser')
		if ifFirstPage == "True":
			OriginaPostAsList = scrapOriginalPostDetails(soupObj,author_name,url_to_scrap,postType)
			# [{"Author_name": "Dharani", "Post_text": "...."}]
			UserPostEntries = scrapPostDetails(soupObj,url_to_scrap,postType)
			# [	{"Author_name": "Dharani", "Post_text": "...."},
			# 	{"Author_name": "Dharani", "Post_text": "....""},
			# ]
			pagePosts.extend(OriginaPostAsList)
			pagePosts.extend(UserPostEntries)
			for item in pagePosts:
				dictWriter.writerow(item)
		else:
			pagePosts=scrapPostDetails(soupObj,url_to_scrap,postType)
			for item in pagePosts:
				dictWriter.writerow(item)
	else:
		print("Error Link", url_to_scrap)
		errorCount = errorCount + 1
		print(("Error Count %s")%(errorCount))
	print(("Fetching in progress, completed %s")%(int(counter)/TotalCount * 100))
	counter +=1
# # Joined:\s+[a-z,A-Z]{3}\s\d+

"""
Posts:
      1903,000
Posts:
      19,030
Joined:
      Sep 2007
"""