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


# generating url to open the search result
def insta_search(word):
    url = 'https://www.instagram.com/explore/tags/{}/'.format(word)
        # OR url = 'https//www.instagram.com/explore/tags/' + word #
    return(url)


# open the search result
word = 'klfoodie'
url = insta_search(word)
driver.get(url)
time.sleep(8)
    # to avoid the potential error of taking 'page_source' before loading the page


# pick the first post of the page screen
def select_first(driver):
    first = driver.find_element(By.CSS_SELECTOR, 'div._aagu')
    first.click()
    time.sleep(5)
    
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
    except:
        content = ' '
    
    # tag
    tag = re.findall(r'#[^\s#,\\]+', content)
    
    # date
    date = soup.select('time')[0]['datetime'][:10]

    # place
    try: 
        place = soup.select('div._aaql')[0].text
        place = unicodedata.normalize('NFC', content)
    except:
        place = ''
    
    # save the collected html information from above codes
    data = [content, tag, date, place]
    return(data)

get_content(driver)


# move to the next: 'target = n|target(no. of contents for crawling)'
def move_next(driver):
    right = driver.find_element(By.CSS_SELECTOR, "div._aaqg._aaqh > button")
    right.click()
    time.sleep(5)
move_next(driver)


# def of crawling process -- extract the data!
url = insta_search(word)
driver.get(url)
time.sleep(5)
    
    # select first picture
select_first(driver)
time.sleep(3)

result = []
target = 5

for i in range(target):
    try:
        # collect contents
        data = get_content(driver)
        result.append(data)
        move_next(driver)
    except:
        time.sleep(5)
        move_next(driver)
        time.sleep(3)


# save the data
result_df = pd.DataFrame(result)
result_df.columns = ['content', 'tag', 'date', 'place']

# the name of the data
result_df.to_excel(excel_writer='testData.xlsx')


# integrating data
klfoodie_insta_df = pd.DataFrame( [ ] )

folder = './file/'
f_list = ['testData.xlsx.xlsx', '1_crawling_jejudoGwanGwang.xlsx', '1_crawling_jejuMatJip.xlsx', '1_crawling_jejuYeoHang.xlsx']

for frame in f_list:
    fpath = folder + frame
    temp = pd.read_excel(fpath)
    klfoodie_insta_df = klfoodie_insta_df.append(temp)

klfoodie_insta_df.coluns = ['content', 'tag', 'date', 'place']


# removing repeated data
klfoodie_insta_df.drop_duplicates(subset = [ "content"] , inplace = True)
klfoodie_insta_df.to_excel('./file/1_crawling_raw.xlsx', index = False)


