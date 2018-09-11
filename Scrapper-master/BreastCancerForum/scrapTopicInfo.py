from bs4 import BeautifulSoup as bs
import requests


home_url = "https://community.breastcancer.org/"
start_page = "forum/8?page=1"
url_list_to_scrap = []


forum_url = home_url+start_page


# r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
r = requests.get(forum_url)


html_code = r.text


soup =  bs(html_code,'html.parser')




rowgroup_ul =  soup.find_all("ul",class_="rowgroup")
list_elm = rowgroup_ul[0].findChildren("li")

for elem in list_elm:
    # print(elem)
    print("--------------\n\n\n")

    para = elem.find_all("p")
    href = elem.find("a")

    # print(para.span.strong.text)
    print(para)
    print(href.get("href"))


paging_div = soup.find("div",class_="paging")
pagination = paging_div.findChildren("div",class_="pagination")

print(pagination)
#See if there is a last pagination in the page.
