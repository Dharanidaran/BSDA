from bs4 import BeautifulSoup as bs
import requests
import re
import time
import csv

class CancerForum:
    def __init__(self):
        self.homePageUrl = "https://community.breastcancer.org/"
        self.firstPageRelUrl = "forum/8?page=1"
        self.pageCount = 722
        self.pageUrl = []
        self.topic_details_list = []
        self.delimiter = ";"
        self.datePattern = re.compile(r"""
                                (?P<Created>\w{3}\s+\d+,\s\d+\s\d+:\d+[AP]M) # Created On
                                """,re.VERBOSE
                            )
        self.generatePageLinks(self.pageCount)


    # def writePageLinkToFile(self):



    def generatePageLinks(self, pageCount):
        # This function will genertate the page url where we can find the
        # Topics overview and not the entire discussion itself
        # For example
        # https://community.breastcancer.org/forum/8?page=0
        # https://community.breastcancer.org/forum/8?page=1
        # https://community.breastcancer.org/forum/8?page=2
        # https://community.breastcancer.org/forum/8?page=3
        # https://community.breastcancer.org/forum/8?page=4
        fieldnames = ["Topic_title","Topic_type","Topic_link",
                        "Author_name","Author_Url","Link_id","Created_date",
                        "Last_posted","Fetch_status","Post_count","Post_views"] #Convert dict keys to list
        filename = "Discussion.csv"
        fp = open(filename,'w')
        csvwriter = csv.DictWriter(fp,fieldnames = fieldnames,delimiter = self.delimiter)
        csvwriter.writeheader()

        for pageNo in range(1,pageCount):
            url = self.homePageUrl+"forum/8?page=%s"%pageNo
            print(url)
            self.pageUrl.append(url)
            topic_details_list = self.getTheDiscussionTopicDetails(url)
            for item in self.topic_details_list:
                print(item["Topic_title"])
                csvwriter.writerow(item)
            time.sleep(1)

    def getTheCreatedLastUpdatedDate(self, html_string):
        matches =  self.datePattern.finditer(html_string)
        counter = 0
        Created_date = None
        Updated_date = None
        for match in matches:
            if counter == 0:
                Created_date = match.group()
            else:
                Updated_date = match.group()
            counter +=1

        if Created_date == None:
            Created_date = "Recent Post"

        if Updated_date == None:
            Updated_date = "Last Posted Recently"



        return (Created_date,Updated_date)



    def getTheDiscussionTopicDetails(self, url):
        # This function will return the list of topics discussed for the
        # given url. For example like
        # Topic Name
        # TotalNo Of Post
        # CreatedBy
        # Time
        # Author
        # Url to the topic pageNo
        # Post Type
        #Add the details to self.topic_details_list
        r = requests.get(url)
        html_code = r.text
        soup =  bs(html_code,'html.parser')
        rowgroup_ul = soup.find("ul",class_="rowgroup")
        list_elms = rowgroup_ul.findChildren("li") #Returns an array of list elm


        for elem in list_elms:
            topic_dict = {}
            # para = elem.find_all("p")

            header = elem.find("h3")
            a = header.find("a")

            created_date,updated_date = self.getTheCreatedLastUpdatedDate(elem.text)

            author_name = None
            author_link = None
            author_details = None
            post_count = elem.find("span",{"class": "count-posts"}).find("strong").text
            post_views = elem.find("span",{"class": "count-views"}).find("strong").text
            try:
                relative_href = a.get("href")
                link_id = relative_href.split("/")[-1]
                topicType = a.get("class") #Returns a list of class names
                title = a.text.replace(";","")
                lastSpanElem = elem.find_all("span")[-1]
                author_details = lastSpanElem.find("a")

                author_name =  author_details.text
                author_link = self.homePageUrl+author_details.get("href")
                fetch_status = "Good"
            except:
                fetch_status = "Error"



            try:
                topic_dict["Topic_title"] = title
                topic_dict["Topic_type"] = topicType
                topic_dict["Topic_link"] = self.homePageUrl+"%s"%relative_href
                topic_dict["Author_name"] =  author_name
                topic_dict["Author_Url"] =  author_link
                topic_dict["Link_id"] = link_id
                topic_dict["Created_date"] = created_date
                topic_dict["Last_posted"] = updated_date
                topic_dict["Fetch_status"] = fetch_status
                topic_dict["Post_count"] = post_count
                topic_dict["Post_views"] = post_views
            except:
                topic_dict["Topic_title"] = title
                topic_dict["Topic_type"] = "Error"
                topic_dict["Topic_link"] = self.homePageUrl+"%s"%relative_href
                topic_dict["Post_count"] = post_count
                topic_dict["Author_name"] =  "Error"
                topic_dict["Author_Url"] =  "Error"
                topic_dict["Link_id"] = "Error"
                topic_dict["Created_date"] = "Error"
                topic_dict["Last_posted"] = "Error"
                topic_dict["Fetch_status"] = "Error"
                topic_dict["Post_views"] = post_views
            #Add the details to self.topic_details_list
            self.topic_details_list.append(topic_dict)

forum = CancerForum()
