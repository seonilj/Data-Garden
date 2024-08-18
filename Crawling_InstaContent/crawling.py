from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

import pandas as pd
import numpy as np
import time

import re
import unicodedata # to avoid broken texts from Mac

# open and Login to instagram
url = 'https://instagram.com/'
driver = webdriver.Chrome()

driver.get(url)
time.sleep(20)


# login --- currently skip


# URL: generating url to open the search result
##########
def insta_search(word):
    url = 'https://www.instagram.com/explore/tags/{}/'.format(word)
        # OR url = 'https//www.instagram.com/explore/tags/' + word #
    return(url)
##########


# open the search result
##########
word = 'KEYWORD'
##########
url = insta_search(word)
driver.get(url)
time.sleep(5)
    # to avoid the potential error of taking 'page_source' before loading the page


# pick the first post of the page screen
def select_first(driver):
    first = driver.find_element(By.CSS_SELECTOR, 'div.x9i3mqj')
    first.click()
    time.sleep(3)
    
select_first(driver)


# def by integrating above html information
def get_content(driver):
    
    # taking html info of the current webpage
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # date
    date = soup.select('time')[0]['datetime'][:10]
    
    # content
    try:
        content = soup.select('div._a9zs > h1')[0].text  
        content = unicodedata.normalize('NFC', content) 
    except:
        content = ''
    
    # tag
    tag = re.findall(r'#[^\s#,\\]+', content)
    
    # save the collected html information from above codes
    data = [date, tag, content]
    return(data)

get_content(driver)


# move to the next: 'target = n|target (how many contents for crawling)'
def move_next(driver):
    right = driver.find_element(By.CSS_SELECTOR, "div._aaqg._aaqh > button")
    right.click()
    time.sleep(3)
move_next(driver)


# def of crawling process -- extract the data!
url = insta_search(word)
driver.get(url)
time.sleep(5)

# select first picture
select_first(driver)
time.sleep(3)

result = []
##########
target = 3
##########

for i in range(target):
    try:
        # collect contents
        data = get_content(driver)
        result.append(data)
        move_next(driver)
    except:
        time.sleep(3)
        move_next(driver)
        time.sleep(3)


# save the data
result_df = pd.DataFrame(result)
result_df.columns = ['date', 'tag', 'content']
########## the name of the data
result_df.to_excel(excel_writer='./RESULT.xlsx',
                   index = False) # to remove auto row numbers
##########