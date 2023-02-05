from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
from Variables import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from config import *


def Get_Users(pages):
    urls, names = [],[]
    
    p_num = 1
    while p_num <= pages:
        sleep(2)
        browser.get(f'https://www.linkedin.com/search/results/people/?geoUrn="{geoUrn}"&keywords={keyword}&page={p_num}')

        sleep(5)
        soup = BeautifulSoup(browser.page_source, features="html.parser")
        pav = soup.find("ul", {"class": "reusable-search__entity-result-list list-style-none"})
        pav = pav.findAll("li", {"class": "reusable-search__result-container"})

        for i in pav:
            d1 = i.find("div", {"class": "t-roman t-sans"})
            d1 = d1.find("span", {"class": "entity-result__title-text t-16"})
            links = d1.find("a",{"class":"app-aware-link"})
            urls.append(links.get("href"))
            name = links.find("span")
            name = name.find("span").text
            names.append(name)
        p_num+=1
    
    nNames = []
    for i in names[:len(urls)]:
        firstName = i.split(" ")
        nNames.append(firstName[0])

    data = {"Name": nNames, "Profile_Url": urls}
    return data

# LinkedIn Login
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))
browser.get('https://www.linkedin.com/uas/login')

sleep(2)
elementID = browser.find_element(By.ID,'username')
elementID.send_keys(username)

elementID = browser.find_element(By.ID,'password')
elementID.send_keys(password)

sleep(2)
elementID.submit()

# Getting User Data
sleep(2)
userData = Get_Users(numberOfUsers/10)


# Sending Message to Users
for i, name in zip(userData['Profile_Url'], userData['Name']):
    grp = None
    try:
        browser.get(i)
        sleep(2)
        soup = BeautifulSoup(browser.page_source, features="html.parser")
        grp = soup.find("div", {'class': "pvs-profile-actions"})
        text = grp.findAll('span', {"class":"artdeco-button__text"})[-1].text
        if text == "\n    Connect\n":
            connect = browser.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[1]/button")
            ActionChains(browser).move_to_element(connect).click(connect).perform()

            sleep(2)
            add_note = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[1]")
            ActionChains(browser).move_to_element(add_note).click(add_note).perform()

            sleep(2)
            textfield = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div[1]/textarea")
            textfield.send_keys(Message(name))
            if enableMessageSent:
                sleep(1)
                sendMessage = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]")
                ActionChains(browser).move_to_element(sendMessage).click(sendMessage).perform()
    
        if text == "\n    Pending\n":
            continue

        if text == "\n    Save in Sales Navigator\n":
            sleep(2)
            browser.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button").click()
            browser.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[5]/div").click()
            sleep(1)
            browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/div/button[1]").click()
            sleep(1)
            browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button").click()
            browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button[1]").click()
            sleep(1)    
            textfield = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div[1]/textarea")
            textfield.send_keys(Message(name))
            sleep(1)
            sendMessage = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]")
            ActionChains(browser).move_to_element(sendMessage).click(sendMessage).perform()  

        else:
            try:
                sleep(2)
                browser.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[3]/button").click()
                sleep(1)
                try:
                    browser.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[3]/div/div/ul/li[3]/div").click()
                except:
                    browser.find_element(By.XPATH,"/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button").click()

                sleep(1)
                try:
                    browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button[1]").click()

                    sleep(1)    
                    textfield = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div[1]/textarea")
                    textfield.send_keys(Message(name))
                    if enableMessageSent:
                        sleep(1)
                        sendMessage = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]")
                        ActionChains(browser).move_to_element(sendMessage).click(sendMessage).perform()        
                except:
                    browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/div/button[1]").click()
                    sleep(1)
                    browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button").click()
                    browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button[1]").click()

                    sleep(1)    
                    textfield = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div[1]/textarea")
                    textfield.send_keys(Message(name))
                    if enableMessageSent:
                        sleep(1)
                        sendMessage = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]")
                        ActionChains(browser).move_to_element(sendMessage).click(sendMessage).perform() 
            except:
                sleep(2)
                browser.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/button").click()
                browser.find_element(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/div[2]/div/div/ul/li[5]/div").click()
                sleep(1)
                browser.find_element(By.XPATH,"/html/body/div[3]/div/div/div[3]/button[1]").click()
                sleep(1)    
                textfield = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div[1]/textarea")
                textfield.send_keys(Message(name))
                sleep(1)
                sendMessage = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div[3]/button[2]")
                ActionChains(browser).move_to_element(sendMessage).click(sendMessage).perform()                              
    except:
        pass






