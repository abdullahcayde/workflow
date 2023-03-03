import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import numpy as np


#Define functions
# Sleep function 
def sleep(x):
    time.sleep(x)

# Wait for a certain measure of time before throwing an exception
def wait(x):
    driver.implicitly_wait(x)

# Click Function
def click_bann_byID(ID):
    actions = ActionChains(driver)
    akzeptieren = driver.find_element(By.ID, ID)
    actions.click(akzeptieren).perform()
    wait(10)
    sleep(0.5)

# Find Elements Function
def find_elements_HPCO(H,P,C,O):
    if website_name == 'jobware':
        header = driver.find_elements(By.TAG_NAME, H)
    else:
        header = driver.find_elements(By.CLASS_NAME, H)
    publish = driver.find_elements(By.CLASS_NAME, P)
    company = driver.find_elements(By.CLASS_NAME, C)
    ort = driver.find_elements(By.CLASS_NAME, O) 

    list_header = [title.text for title in header]
    list_publish = [pub.text for pub in publish]
    list_company = [comp.text for comp in company]
    list_ort = [o.text for o in ort]
    return list_header, list_publish, list_company, list_ort

# Scroll Down Function
def scroll_down(x):
    n=0
    while n < x:
        n+=1
        actions.key_down(Keys.PAGE_DOWN).perform()
        sleep(1.5)
        actions.key_down(Keys.PAGE_DOWN).perform()
        sleep(1.5)
        actions.key_down(Keys.PAGE_DOWN).perform()
        sleep(1.5)
        actions.key_down(Keys.PAGE_UP).perform()
        sleep(0.10)
        actions.key_down(Keys.PAGE_DOWN).perform()
        wait(10)
        sleep(2.5)
        
        
'''
Title : Web Scrapping by Selenium 
Project Purpose: From StepStone scrap data for some Job Titels
1 - Create Driver
2 - Go to Website
3 - Create ActionChain Object
    3.1 - Click Banned 
4 - Take Title and Infos from Page
    4.1 - Create Lists 
    4.2 - Create DataFrame
    4.3 - Repeat Process
    4.4 - Print and Save DataFrame
'''

print('---------------------- StepStone Job Searching Selenium Project ----------------------')
start=datetime.now()  
# Link Descriptions
link_original_stepstone = 'https://www.stepstone.de/jobs/data-analyst/in-rietberg?radius=50&page=2'

website_name = 'stepstone'
job_name = 'Business Analyst'
#job_name = 'Data Analyst'
#job_name = 'Data Scientist'
ort_ = 'Rietberg'
radius = 50
page_number = 1

#  1 - Create Driver
Path = '/Users/macbook/Desktop/projects/Github_Repositories/Portfolio Projects/02 - Web_Scraping_Job_Search/chromedriver'
driver = webdriver.Chrome(Path)

#  2 - Go to Website
job_link = job_name.replace(' ', '-').lower()
ort_link = ort_.lower()
link = f'https://www.stepstone.de/jobs/{job_link}/in-{ort_link}?radius={radius}&page={page_number}'

driver.get(link)
wait(10)
sleep(2)

#  3 - ActionChain Object created
# 3.1 - Click Banned Accept
ID = 'ccmgt_explicit_accept'
click_bann_byID(ID)


# 4 -  Take Infos from Page
# 4.1 - Headers, Publish_Time ,Company, City
H, P, C, O = 'resultlist-1uvdp0v', 'resultlist-w7zbt7', 'resultlist-1va1dj8', 'resultlist-suri3e'
list_header, list_publish, list_company, list_ort = find_elements_HPCO(H,P,C,O)

# 4.2 - Description and Page number of results
description = driver.find_elements(By.CLASS_NAME, 'resultlist-1fp8oay')
result = driver.find_elements(By.CLASS_NAME, 'resultlist-1jx3vjx')


# 4.3 - Get Links
header = driver.find_elements(By.CLASS_NAME, H)
list_link = [link.get_attribute('href') for link in header]

# 4.4 - Get Texts for each finding
list_description = [des.text for des in description]
print('Header',len(list_header), 'Publish',len(list_publish), 'Company',len(list_company[1:]), 'Ort',len(list_ort), 'Desc', len(list_description), 'Link',len(list_link))

# 4.5 - Total Search Page Number
list_result = [res.text for res in result]
number_of_page = int(list_result[-2])
print(f'Number of Jobs Pages = {number_of_page}')

# 4.6 - DataFrame df
d = dict(job_title=np.array(list_header), publish=np.array(list_publish), company=np.array(list_company[1:]), city=np.array(list_ort) , description=np.array(list_description), link=np.array(list_link))
df = pd.DataFrame.from_dict(d, orient='index')
df = df.T


# 4.7 Repeat Process for every Web Page
while  page_number < number_of_page:
    page_number+=1
    
    # 4.7.1 - Go to another page
    link = f'https://www.stepstone.de/jobs/{job_link}/in-{ort_link}?radius={radius}&page={page_number}'
    driver.get(link)
    wait(10)
    sleep(1.5)
    
    # 4.7.2 - Find the elements and get the Texts
    list_header, list_publish, list_company, list_ort = find_elements_HPCO(H,P,C,O) 
    description = driver.find_elements(By.CLASS_NAME, 'resultlist-1pq4x2u')
    list_description = [des.text for des in description]
    header = driver.find_elements(By.CLASS_NAME, H)
    list_link = [link.get_attribute('href') for link in header]
 
    # 4.7.3 - Create new page Dataframe
    d = dict(job_title=np.array(list_header), publish=np.array(list_publish), company=np.array(list_company[1:]), city=np.array(list_ort) , description=np.array(list_description), link=np.array(list_link))
    df2 = pd.DataFrame.from_dict(d, orient='index')
    df2 = df2.T
    
    # 4.7.4 - Concatenate the DataFrames
    df = pd.concat([df,df2], axis=0, ignore_index=True)
    print(f'Page Number : {page_number}, DataFrame Shape : {df2.shape}')
    

# 5.1 - Save Data as csv 
print(f'DataFrame End : {df.shape}')
df['website'] = website_name
time_ = datetime.today().strftime('%Y-%m-%d')
df['date'] = time_
job_name2 = job_name.replace(' ', '_')
df['search_title'] = job_name2

path = '/Users/macbook/Desktop/projects/Github_Repositories/Portfolio Projects/02 - Web_Scraping_Job_Search/data'
job_name3 = job_name.replace(' ', '-')
time_ = datetime.today().strftime('%Y-%m-%d')
df.to_csv(f'{path}/{job_name3}-{time_}.csv', index=False)

# 6 - Quit
end =datetime.now() 
print('Code Runned No Problem')
print(f'Time = {end - start}')
sleep(5)
driver.quit()