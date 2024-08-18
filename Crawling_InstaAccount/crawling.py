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
def insta_search(account):
    url = 'https://www.instagram.com/{}/'.format(account)
        # OR url = 'https//www.instagram.com/' + account #
    return(url)
##########


# open the search result
##########
account = 'kl.foodie'
##########
url = insta_search(account)
driver.get(url)
time.sleep(5)
    # to avoid the potential error of taking 'page_source' before loading the page


# pick the first post of the page screen
def select_first(driver):
    first = driver.find_element(By.CSS_SELECTOR, 'div._aagw')
    first.click()
    time.sleep(3)
    
select_first(driver)


# def by integrating above html information
def get_content(driver):
    
    # taking html info of the current webpage
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # content
    try:
        content = soup.select('div._a9zs > h1')[0].text  
        content = unicodedata.normalize('NFC', content)
        # the account content with events always has below emoji! 
        if '🗓️' not in content:
            content = ''
    except:
        content = ''
    
    # tag
    try:
        tag = re.findall(r'#[^\s#,\\]+', content)
        if '🗓️' not in content:
            tag = ''
    except:
        content = ''
    
    # date
    try:
        date = soup.select('time')[0]['datetime'][:10]
        if '🗓️' not in content:
            date = ''
    except:
        content = ''
    
    # save the collected html information from above codes
    data = [date, tag, content]
    return(data)

get_content(driver)


# move to the next: 'target = n|target (how many contents for crawling)'
def move_next(driver):
    right = driver.find_element(By.CSS_SELECTOR, "div._aaqg > button")
    right.click()
    time.sleep(3)
move_next(driver)


# def of crawling process -- extract the data!
url = insta_search(account)
driver.get(url)
time.sleep(5)

# select first picture
select_first(driver)
time.sleep(3)

result = []
##########
target = 25
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
result_df = result_df[(result_df != '') & (result_df != ' ')].dropna(how='all').reset_index(drop=True)
########## the name of the data
result_df.to_excel(excel_writer='./Crawling_InstaAccount/RESULT.xlsx',
                   index = False) # to remove auto row numbers
##########


