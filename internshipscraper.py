from operator import contains
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import re
import pandas as pd




#Fetsh the URL
#result = requests.get("https://www.opportunitiescircle.com/internships/")

page_num = 1

def get_page_num(soup):
    nav_pg = soup.find("nav",{"class":"elementor-pagination"})
    pg_nbrs1 = nav_pg.find_all("span",{"class":re.compile("page-numbers")})
    pg_nbrs2 = nav_pg.find_all("a",{"class":re.compile("page-numbers")})
    pg_nbrs = pg_nbrs1 + pg_nbrs2

    return pg_nbrs

lintern = [] #internships_list
cl = [] #countries_list
fl = [] #fundings_list
dl = [] #deadlines_list
ll = [] #links_list

while True: 
    result = requests.get(f"https://www.opportunitiescircle.com/internships/page/{page_num}/")

    #Save page content/markup
    src = result.content
    #print(src)

    #Create soup object to parse content
    soup = BeautifulSoup(src,"lxml")
    '''
    pg_nums=get_page_num(soup)
    #print(pg_nums)

    pg_nbr_list = []
    for i in range(len(pg_nums)):
        pg_nbr_list.append(pg_nums[i].text.strip())
    print(pg_nbr_list)

    pg_nbr_list = [w.replace('Page', '') for w in pg_nbr_list]
    #print(pg_nbr_list)
    n=len(pg_nbr_list)
    #print(n)
    #print(pg_nbr_list[n-2])
    page_limit = int(pg_nbr_list[n-2])
    '''
    
    if(page_num>4):
        print("pages ended")
        break

    # Find the elements containing the infos needed
    # InternshipTitle, Country, Funding, Deadline, OpportunityLink
    # Criterias, Benefits, OfficialLink
    internship_titles = soup.find_all("h3",{"class":"elementor-heading-title elementor-size-default"})
    #print(internship_titles)

    #containers = soup.find_all("div",{"class":"elementor-element elementor-element-a7388c1 elementor-align-center elementor-widget elementor-widget-post-info"})
    containers = soup.find_all("div",{"class":"elementor-column elementor-col-100 elementor-top-column elementor-element elementor-element-bf3ac07"})

    for i in range(len(containers)):
        try:
            cl.append(containers[i].find_all('span',{"class":"elementor-post-info__terms-list"})[0].text.strip())
        except :
            cl.append('Different')
        try:
            fl.append(containers[i].find_all('span',{"class":"elementor-post-info__terms-list"})[1].text.strip())
        except :
            fl.append('Different')
        try:
            dl.append(containers[i].find_all("span",{"class":"elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-custom"})[0].text.strip())
        except :
            dl.append('Different')

    for i in range(len(internship_titles)):
        lintern.append(internship_titles[i].text.strip())
        ll.append(internship_titles[i].find("a").attrs['href'])

    print('li= ',lintern)
    #print(len(containers))
    #print('cl= ',cl)
    #print('fl= ',fl)
    #print('dl= ',dl)
    #print('ll= ',ll)
    print(len(lintern),len(cl),len(fl),len(dl),len(ll))

    page_num +=1
    print('page switched')

print(len(lintern),len(cl),len(fl),len(dl),len(ll))

# Get more infos from each specifi opportunity page
    # Criterias, Benefits, OfficialLink
criteria_list = []
benefits_list = []
officiallink_list = []

for link in ll:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src,"lxml")
    print(link)

    crl = soup.find("div",{"class":"elementor-element elementor-element-d78a9e1 elementor-widget elementor-widget-text-editor"}).ul
    #print(crl)
    criterias_text =""
    try:
        for li in crl.find_all("li"):
            criterias_text += li.text+" | "
            criterias_text = criterias_text[:-2] #delete tha last '|' 
            #print(li)
    except :
            crl = soup.find("div",{"class":"elementor-element elementor-element-d78a9e1 elementor-widget elementor-widget-text-editor"}).p
            #print(crl)
            criterias_text =""
            for li in crl:
                criterias_text += li.text+" | "
                criterias_text = criterias_text[:-2] #delete tha last '|' 
                #print(li)

    bnl = soup.find("div",{"class":"elementor-element elementor-element-004e374 elementor-widget elementor-widget-text-editor"}).ul
    benefits_text =""
    try:
        for li in bnl.find_all("li"):
            benefits_text += li.text+" | "
            benefits_text = benefits_text[:-2]
    except:
            bnl = soup.find("div",{"class":"elementor-element elementor-element-004e374 elementor-widget elementor-widget-text-editor"}).p
            #print(crl)
            criterias_text =""
            for li in crl:
                benefits_text += li.text+" | "
                benefits_text = criterias_text[:-2] #delete tha last '|' 
                #print(li)    

    ofl = soup.find("div",{"class":"elementor-element elementor-element-0cb5de2 elementor-button-info elementor-tablet-align-center elementor-mobile-align-center elementor-widget elementor-widget-button"}).a.attrs['href']
    #ll.append(internship_titles[i].find("a").attrs['href'])
 
    criteria_list.append(criterias_text)
    benefits_list.append(benefits_text)
    officiallink_list.append(ofl)


data_frame = pd.DataFrame(list(zip(lintern,cl, fl, dl,ll,criteria_list,benefits_list,officiallink_list)),columns=['Internship','Country', 'Funding', 'Deadline','Link','Criterias','Benefits','Official Site'])
print(data_frame)


# Generate the csv file
#create data columns to fill the file
'''

zip_longest function

x = [1,2,3]
y = ['a','b','c']
z = [x,y]
*z ---> [[1,2,3],['a','b','c']]
zip_longest(*z) ----> [[1,'a'],[2,'b'],[3,'c']]
'''


file_list = [lintern,cl, fl, dl,ll,criteria_list,benefits_list,officiallink_list]
rw_list = zip_longest(*file_list)
#f=open("test.txt", "w+", encoding="utf-8")

#create the csv file & fill it with the data
with open("C:/2023_insea/DataScience_Prjct/web_scrapping/intershipsScraped.csv","w",encoding="utf-8") as file:
    wr = csv.writer(file)
    wr.writerow(['Internship','Country', 'Funding', 'Deadline','Link','Criterias','Benefits','Official Site'])
    wr.writerows(rw_list)


