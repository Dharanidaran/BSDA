import requests
import re
import time
import csv
import os

class FetchPostComment:
    def __init__(self):
        self.postsPerPage = 30
        self.topicsLinkBuffer = []
        self.filepath =  os.getcwd()+"/TopicStore/NonDuplicate.csv"
        self.readThroughTopicsBuffer()
        self.readTheFile()

    def traversePageUrlList(self,postCount,topicUrl):
        #Return how many pages to traverse if there are many comments
        NoOfPages = None
        UrlToTraverse = []
        if postCount % self.postsPerPage == 0:
            NoOfPages = int(postCount/self.postsPerPage)
        else:
            NoOfPages = int(postCount/self.postsPerPage)+ 1
        #Generate Url
        for item in range(NoOfPages):
            if item == 0:
                UrlToTraverse.append(  ("%s?page=%s"%(topicUrl,item+1),True ) )
            else:
                UrlToTraverse.append(  ("%s?page=%s"%(topicUrl,item+1),False) )
        return UrlToTraverse

    def readTheFile(self):
        fp = open(self.filepath)
        csvReader =  csv.reader(fp,delimiter=";")
        counter1 = 1
        next(fp) #Skipping the header
        for row in csvReader:
            postCount = row[9].replace(",","")
            postId = row[5]
            topicUrl = row[2]
            postType = row[1]
            authorName = row[3]

            for item in self.traversePageUrlList(int(postCount),topicUrl):
                print(("%s;%s;%s;%s;%s;%s")%(counter1,postId,postType,item[0],item[1],authorName))
                counter1 =  counter1+1
    def readThroughTopicsBuffer(self):
        # print(self.filepath)
        pass

fetch = FetchPostComment()

