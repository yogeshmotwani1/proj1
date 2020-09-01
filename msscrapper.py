import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display
import csv
import re
from datetime import date, timedelta, datetime
import datetime
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time 


# https://www.mouthshut.com/search/prodsrch.aspx?data=indigo%20airlines&type=&p=0-srch
# https://www.mouthshut.com/search/prodsrch.aspx?data=jio%20fiber&type=&p=0-srch


# data structures to store scrapped data
user_name = [] 
star = [] # stars out of 5
title = [] 
review = []
address = [] 
views = [] # no of views on a post
total_reviews = [] # no of reviews user has made
no_of_followers = [] # no of followers person has
is_comment = [] # whether the post is comment or review
no_of_days_before = [] # no of days before the post was made
no_of_likes=[] 
list_of_urls = []
list_of_products = []

def fetch_current_page(driver):
    time.sleep(10)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    try:
        full_comment = soup.findAll('div', class_='rtitle')
        for i in range(0,len(full_comment)):
            list_of_urls.append(full_comment[i].find('a')['href'])
            list_of_products.append(full_comment[i].find('a').text)

    except:
        pass
    
    try:
        driver.find_element_by_xpath('//li[@class="page-item next"]/a').click()
        fetch_current_page(driver)
    except:
        pass


def fetch_products_link(company):
    separator = "%20"
    company_in_url = separator.join(company.split(" "))
    link = "https://www.mouthshut.com/search/prodsrch.aspx?data=" + str(company_in_url) + "&type=&p=0-srch"
    driver.get(link)
    fetch_current_page(driver)
    

#function to calculate number of days from various types of data
def count_no_of_days(time_given):
    if(time_given[-1] == 'ago'):
        if('days' in time_given):
            no_of_days_before.append(time_given[0])
        else:
            no_of_days_before.append("0")
    else:
        # if date is given we substract with todays date.
        separator = "-"
        date_given = separator.join(time_given[0:3])
        date_formated = datetime.datetime.strptime(date_given, "%b-%d,-%Y")
        no_of_days_before.append(datetime.datetime.today() - date_formated)
    

def scrap_ms_link(link):

    # to go on the top in the browser
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    
    driver.get(link)

    # to fetch no. of posts in the page
    comment_links = re.findall("Comments [0-9]+",str(driver.page_source))

    #clicking all Read More buttons
    for i in range(0, len(driver.find_elements_by_link_text("Read More"))):
        driver.find_element_by_link_text("Read More").click()

    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(3)

    # clicking all comment buttons    
    for i in range(0,len(comment_links)):
        time.sleep(1)
        if(len(str(i))==1):
            driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl"+"0"+str(i)+"_commentspan").click()
        else:
            driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl"+str(i)+"_commentspan").click()
        


    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    for i in range(0, len(driver.find_elements_by_link_text("Read More"))):
        driver.find_element_by_link_text("Read More").click()

    #clicking all read more comments if found
    for i in range(0,len(comment_links)):
        try:
            if(len(str(i))==1):
                driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl"+"0"+str(i)+"_linkpostcomment").click()
            else:
                driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_rptreviews_ctl"+str(i)+"_linkpostcomment").click()
        except:
            pass

# -------------selenium part done now beautifulsoup part starts---------------

    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    #fetching all posts and storing in the list.
    full_review = soup.findAll('div', class_='row review-article')

    for i in range(0,len(full_review)):
        #fetching all the data of posts and storing in the datastructures declared
        user_name.append(str(full_review[i].find('div', class_='user-ms-name').find('a').text))
        star.append(str(len(full_review[i].find('div',class_='rating').span.findAll('i',class_='icon-rating rated-star'))))
        title.append(str(full_review[i].find('strong').text))
        review.append(str(full_review[i].find('div',class_='more reviewdata').text))
        address.append(str(full_review[i].find('div',class_='usr-addr-text').text).replace("=- ", ""))
        views.append(full_review[i].find('span',class_='views').text.split(" ")[0].split('+')[0])
        total_reviews.append(full_review[i].find('div',class_='total-rev-counts').find('a').text.split(" ")[0])
        is_comment.append("False")
        no_of_likes.append(full_review[i].find('div',class_='tooltip like-count').find('a').text)

        #fetching time and passing to the function to calculate the days left
        time_given = full_review[i].find('div',class_='rating').find_all('span')[1].text.split(" ")
        count_no_of_days(time_given)
        
        try:
            no_of_followers.append(full_review[i].find('div',class_='total-followers-counts').find('a').text.split(" ")[1])
        except:
            no_of_followers.append("0")

    #fetching all the comments data and storing in the list.
    full_comment = soup.findAll('div', class_='comment hide')

    # fetching all the data of comments and storing in the datastructures declared
    # direct find method was not working was used this below approach
    
    for i in range(1,len(full_comment)):
        a_tags = full_comment[i].findAll('a')
        p_tags = full_comment[i].findAll('p',class_="more lh20")
        span_tags = full_comment[i].findAll('span')

        for j in range(0,len(p_tags)):
            review.append(str(p_tags[j].text))

        for j in range(1,len(a_tags),2):
            user_name.append(str(a_tags[j].text))
        
        for j in range(2,len(span_tags),2):
            time_given = span_tags[j].text.split(" ")
            count_no_of_days(time_given)

        for j in range(0,len(p_tags)):
            is_comment.append("True")
            total_reviews.append("NA")
            views.append("NA")
            address.append("NA")
            star.append("NA")
            title.append("NA")
            no_of_followers.append("NA")
            no_of_likes.append("NA")        
    
    # checking if there is next page. if go to next page and repeat the procedure.
    try:
        next_link = soup.find('li',class_="next").find('a')['href']
        scrap_ms_link(next_link)
        
    except:
        pass


def write_to_csv():
    # initializing fields and rows
    fields = ['User','Is Comment','Review','Followers', 'Stars', 'Title','Address','Views','Total_Reviews','Time','Likes'] 
    rows = []
    for i in range(0,len(user_name)):
        rows.append([user_name[i], is_comment[i], review[i], no_of_followers[i], star[i], title[i], address[i], views[i], total_reviews[i], no_of_days_before[i],no_of_likes[i]])  
    
    # name of csv file 
    filename = "mouthshut.csv"
        
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(rows)
         

# adding some settings of selenium 
op = webdriver.ChromeOptions()
op.add_argument("user-data-dir=./chromeprofile")
op.add_argument("disable-infobars")
op.add_argument("disable-notifications")
driver = webdriver.Chrome(options=op)   

companies = ['one plus', 'jio fiber']
for company in companies:
    fetch_products_link(company)

print(list_of_urls)

# ['yes','no']

for link in list_of_urls:
    scrap_ms_link("https://www.mouthshut.com"+link)

write_to_csv()