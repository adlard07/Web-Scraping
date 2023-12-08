from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time


class Profiles:
    #scrolls till the end of the page returning all the links of profiles
    def get_profiles(self, url, driver):
        driver.get(url)
        while True:
            initial_height = driver.execute_script("return document.body.scrollHeight;")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            updated_height = driver.execute_script("return document.body.scrollHeight;")
            if updated_height == initial_height:
                break
            
            links=[]
            tags = driver.find_elements(By.TAG_NAME, "a")
            for tag in tags:
                value = tag.get_attribute("href")
                links.append(value)
            
        return (
            driver,
            links[::2]
            )
        
    # iterates over the links and returns the final dataframe with all the fields
    def json_output(self, driver, links):
        data = []
        for link in links:
            driver.get(link)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            name = soup.find_all('h2', class_='style__Name-cmp__sc-1s7e137-1 jhjTCw')
            job = soup.find_all('h4', class_='style__Job-cmp__sc-1s7e137-2 dzeTcv')
            org = soup.find_all('h3', class_='style__Organization-cmp__sc-1s7e137-3 cVzOUy')
            
            question = soup.find_all('div', class_='style__Name-cmp__sc-165xmjy-1 dVHQNt')
            answer = soup.find_all('div', class_='style__Content-cmp__sc-165xmjy-2 dNVyzo')
            
            names, jobs, orgs, ques, ans = [], [], [], [], []
            for i in range(len(question)):
                ques.append(question[i].text)
                ans.append(answer[i].text)
            diction = dict(zip(ques, ans))
            
            for i in range(len(name)):
                names.append(name[i].text)
                jobs.append(job[i].text)
                orgs.append(org[i].text)
                
            diction['Name'] = names
            diction['Job title'] = jobs
            diction['Organization'] = orgs
            
            data.append(diction)
        # identifies unique values(questions and answers) and assigns them as column name
        new_data = {}
        all_keys = {key for d in data for key in d}
        new_data = {key: [] for key in all_keys}
        for d in data:
            for key in all_keys:
                new_data[key].append(d.get(key, np.nan))
        
        output = pd.DataFrame(new_data)
            
        return output
    
## test cases
if __name__=="__main__":
    driver = webdriver.Edge()
    url = "https://ocimpact.app.swapcard.com/widget/event/oc2023/people/RXZlbnRWaWV3XzQ1NTQwOA==?showActions=true"
    time.sleep(3)
    
    profiles = Profiles()
    driverr, links = profiles.get_profiles(url, driver)
    
    output = profiles.json_output(driver, links[:5])
    print(output, "\n")
    print(output.columns)