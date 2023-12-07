from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Edge()
url = "https://ocimpact.app.swapcard.com/widget/event/oc2023/people/RXZlbnRWaWV3XzQ1NTQwOA==?showActions=true"
time.sleep(3)

class Profiles:
    def get_profiles(self, url, driver):
        driver.get(url)
        while True:
            initial_height = driver.execute_script("return document.body.scrollHeight;")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            updated_height = driver.execute_script("return document.body.scrollHeight;")
            if updated_height == initial_height:
                break
            name = [driver.find_elements(By.XPATH, '//span[@class="clamp__Clamp-ui__sc-1aq2rfp-0 grid__FullName-cmp__sc-1x1x5ym-3 hAEPUd klXdSC"]')]
            job = [driver.find_elements(By.XPATH, '//span[@class="clamp__Clamp-ui__sc-1aq2rfp-0 grid__Job-cmp__sc-1x1x5ym-5 hAEPUd eXjbIP"]')]
            org = [driver.find_elements(By.XPATH, '//span[@class="clamp__Clamp-ui__sc-1aq2rfp-0 grid__Organization-cmp__sc-1x1x5ym-6 hAEPUd cOiylb"]')]

            links=[]
            tags = driver.find_elements(By.TAG_NAME, "a")
            for tag in tags:
                value = tag.get_attribute("href")
                links.append(value)
        return (
            name,
            job,
            org,
            links
            )
    def json_output(self, name, job, org, links):
        data = []
        for link in links[:5]:
            driver.get(link)
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            question = soup.find_all('div', class_='style__Name-cmp__sc-165xmjy-1 dVHQNt')
            answer = soup.find_all('div', class_='style__Content-cmp__sc-165xmjy-2 dNVyzo')
            
            ques, ans = [], []
            for i in range(len(question)):
                ques.append(question[i].text)
                ans.append(answer[i].text)
            diction = dict(zip(ques, ans))
            data.append(diction)

        if len(name) == len(job) == len(org) == len(links):
            new_data = {}
            for d in data:
                for key, value in d.items():
                    if key not in new_data:
                        new_data[key] = [value]
                    else:
                        new_data[key].append(value)
            new_data['Name'] = name
            new_data['Job title'] = job
            new_data['Organization'] = org
            
            output = pd.DataFrame(new_data)
            
        return output

if __name__=="__main__":

    # links = [
    #     'https://ocimpact.app.swapcard.com/widget/event/oc2023/person/RXZlbnRQZW9wbGVfMjIzMTY3Mjg=', 
    #     'https://ocimpact.app.swapcard.com/widget/event/oc2023/person/RXZlbnRQZW9wbGVfMjU3MTUwMzU=',
    #     'https://ocimpact.app.swapcard.com/widget/event/oc2023/person/RXZlbnRQZW9wbGVfMjUyOTQxMzQ=',
    #     ]
    # name = ['John', 'Alice', 'Bob']
    # job = ['Engineer', 'Manager', 'Developer']
    # org = ['Company A', 'Company B', 'Company C']
    
    profiles = Profiles()
    name, job, org, links = profiles.get_profiles(url, driver)
    output = profiles.json_output(name, job, org, links)
    print(output)