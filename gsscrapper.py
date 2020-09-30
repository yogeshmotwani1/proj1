import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display
import csv
import time
from selenium.webdriver.common.keys import Keys
import io
import xlrd
import re

# user_name = []
star_overall = []
star_worklife = []
star_culture = []
star_career = []
star_compensation = []
star_senior_management = []
title = []
main_text = []
pros_by_author = []
cons_by_author = []
advice_by_author = []
date = []
position = []
location = []
positives_by_author = []
negatives_by_author = []
neutral_by_author = []
def scrap_gs_link(link,flag):
    # time.sleep(3)
    if(len(star_overall)>500):
        return
    driver.get(link)
    time.sleep(5)
    # driver.implicitly_wait(10)
    # print(len(driver.find_elements_by_css_selector("v2__EIReviewDetailsV2__continueReading.v2__EIReviewDetailsV2__clickable")))
    # print(len(driver.find_elements_by_link_text("Continue.reading")))
    print(len(driver.find_elements_by_xpath("//div[contains(text(), 'Continue reading')]")))
    if(flag=="True"):
        print("True")
        try:
            for i in range(0, len(driver.find_elements_by_xpath("//div[contains(text(), 'Continue reading')]"))):
                driver.find_elements_by_xpath("//div[contains(text(), 'Continue reading')]")[i].click()
                time.sleep(1)
                driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        except:
            driver.find_element_by_id("userEmail").send_keys("parshotamprataprai@gmail.com")
            time.sleep(1)
            driver.find_element_by_id("userPassword").send_keys("hotnessis")
            time.sleep(10)
            # driver.find_element_by_css_selector("button.gd-ui-button.minWidthBtn.css-1sdotxz").click()
    try:    
        for i in range(0, len(driver.find_elements_by_xpath("//div[contains(text(), 'Continue reading')]"))):
            driver.find_elements_by_xpath("//div[contains(text(), 'Continue reading')]")[i].click()
            # time.sleep(1)
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    except:
        pass
    try:
        for i in range(0, len(driver.find_elements_by_xpath("//div[contains(text(), 'Continue reading')]"))):
            driver.find_elements_by_xpath("//div[contains(text(), 'Continue reading')]")[i].click()
            # time.sleep(1)
            driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    except:
        pass
    try:
        driver.find_element_by_class_name('reviewLink')
        print("Kya baat hai")
    except:
        return
    source = driver.page_source
    # print(source)
    soup = BeautifulSoup(source, 'html.parser')
    full_review = soup.findAll('li', class_='empReview cf')
    print("Hell yeah")
    for i in range(0,len(full_review)):
        date.append(full_review[i].find('time', class_='date subtle small').text)
        title.append(full_review[i].find('a',class_='reviewLink').text)
        star_overall.append(full_review[i].find('div',class_='v2__EIReviewsRatingsStylesV2__ratingNum v2__EIReviewsRatingsStylesV2__small').text)
        try:
            star_worklife.append(full_review[i].find('ul',class_='undecorated').find_all('li')[0].find('span')['title'])
            star_culture.append(full_review[i].find('ul',class_='undecorated').find_all('li')[1].find('span')['title'])
            star_career.append(full_review[i].find('ul',class_='undecorated').find_all('li')[2].find('span')['title'])
            star_compensation.append(full_review[i].find('ul',class_='undecorated').find_all('li')[3].find('span')['title'])
            star_senior_management.append(full_review[i].find('ul',class_='undecorated').find_all('li')[4].find('span')['title'])
        except:
            star_worklife.append('NA')
            star_culture.append('NA')
            star_career.append('NA')
            star_compensation.append('NA')
            star_senior_management.append('NA')

        position.append(str(full_review[i].find('span',class_='authorJobTitle middle').text))
        try:
            location.append(str(full_review[i].find('span',class_='authorLocation').text))
        except:
            location.append("NA")
        print("Yo")
        try:
            temp_positive = ""
            temp_div = full_review[i].find_all(attrs={'class': 'col-sm-4'})
            # print(temp_div)
            pos_flag = False
            neg_flag = False
            neu_flag = False
            pos_string = ""
            neg_string = ""
            neu_string = ""
            for j in range(0,len(temp_div)):
                try:
                    if(len(temp_div[j].find_all(attrs={'class': 'green'}))>0):
                        # positives_by_author.append(str(temp_div[j].text))
                        pos_string += str(temp_div[j].text) + "  "
                        pos_flag = True
                except:
                    pass
                try:
                    if(len(temp_div[j].find_all(attrs={'class':'red'}))>0):
                        # negatives_by_author.append(str(temp_div[j].text))
                        neg_string +=str(temp_div[j].text) + "  "
                        neg_flag = True
                except:
                    pass
                try:
                    if(len(temp_div[j].find_all(attrs={'class':'yellow'}))>0):
                        neu_string += str(temp_div[j].text) + "  "
                        neu_flag=True
                    # neutral_by_author.append(str(temp_div[j].text))
                except:
                    pass
            if(pos_flag == True):
                positives_by_author.append(pos_string)
            else:
                positives_by_author.append("NA")
            if(neg_flag == True):
                negatives_by_author.append(neg_string)
            else:
                negatives_by_author.append("NA")
            if(neu_flag == True):
                neutral_by_author.append(neu_string)
            else:
                neutral_by_author.append("NA")
                        # temp_div[j].find(attrs={'class':'yellow'})
                        # neutral_by_author.append(str(temp_div[j].text))
        except:
            pass
        try:
            temp_main_text = full_review[i].find('p',class_='mainText mb-0').text
            main_text.append(temp_main_text)
        except:
            main_text.append(temp_main_text)
        try:
            pros_by_author.append(str(full_review[i].find('span', {'data-test':"pros"}).text).replace("=-","").replace('\n'," "))
        except:
            pros_by_author.append('NA')
        try:
            cons_by_author.append(str(full_review[i].find('span', {'data-test':"cons"}).text).replace("=-","").replace('\n'," "))
        except:
            cons_by_author.append('NA')
        try:
            advice_by_author.append(str(full_review[i].find('span', {'data-test':"advice-management"}).text).replace("=-","").replace('\n'," "))
        except:
            advice_by_author.append('NA')
    
    print(str(len(star_overall))+" "+str(len(title))+" "+str(len(main_text))+" "+str(len(pros_by_author))+" "+str(len(cons_by_author))+" "+str(len(advice_by_author))+" "+str(len(date))+" "+str(len(position))+" "+str(len(location))+" "+str(len(positives_by_author))+" "+str(len(negatives_by_author))+" "+str(len(neutral_by_author)))
    try:
        next_link = soup.find('li',class_="pagination__PaginationStyle__next").find('a')['href']
        scrap_gs_link("https://www.glassdoor.co.in"+str(next_link),"False")
        
    except:
        pass
    print(str(len(star_overall))+" "+str(len(title))+" "+str(len(main_text))+" "+str(len(pros_by_author))+" "+str(len(cons_by_author))+" "+str(len(advice_by_author))+" "+str(len(date))+" "+str(len(position))+" "+str(len(location))+" "+str(len(positives_by_author))+" "+str(len(negatives_by_author))+" "+str(len(neutral_by_author)))
    print(positives_by_author)

def write_to_csv():
    fields=['star_overall','star_worklife','star_culture','star_career','star_compensation','star_senior_management','title','main_text','pros_by_author','cons_by_author','advice_by_author','date','position','location','positives_by_author','negatives_by_author','neutrals by author']
    rows = []
    
    for i in range(0,len(star_overall)):
        rows.append([star_overall[i],star_worklife[i],star_culture[i],star_career[i],star_compensation[i],star_senior_management[i],title[i],main_text[i],pros_by_author[i],cons_by_author[i],advice_by_author[i],date[i],position[i],location[i],positives_by_author[i],negatives_by_author[i],neutral_by_author[i]])
    
    filename="potash.csv"
    
    with io.open(filename,'w',encoding="utf-8",newline="") as csvfile:
        #creating a csv writer object
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

op = webdriver.ChromeOptions()
op.add_argument("user-data-dir-./chromeprofile")
op.add_argument("disable-infobars")
op.add_argument("disable-notifications")
driver = webdriver.Chrome(options=op)

scrap_gs_link("https://www.glassdoor.co.in/Reviews/Indian-Potash-Limited-Reviews-E512315.htm","True")
write_to_csv()