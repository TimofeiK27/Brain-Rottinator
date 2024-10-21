from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time, os, json,random ,math
import undetected_chromedriver as uc

from pynput.keyboard import Key, Controller

#Youtube Login
def uploadYoutube(video,email,password,link,TITLE,tags,description):
    print(link)
    driver = uc.Chrome()
    driver.get(link)
    elem = driver.find_element(By.XPATH,'//input')
    elem.send_keys(email)
    time.sleep(1)
    driver.find_element(By.XPATH,'//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b"]').click()
    time.sleep(7)
    elem2 = driver.find_element(By.XPATH,'//input[@type="password"]')
    elem2.send_keys(password)
    time.sleep(1)
    driver.find_element(By.XPATH,'//button[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 BqKGqe Jskylb TrZEUc lw1w4b"]').click()
    time.sleep(5)
    driver.find_element(By.XPATH,'//ytcp-button[@id="create-icon"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//tp-yt-paper-item[@id="text-item-0"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//ytcp-button[@id="select-files-button"]').click()
    time.sleep(1)
    print(video)
    file = os.path.abspath(video)
    keyboard = Controller()
    keyboard.type(file)
    time.sleep(2)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(3)

    if TITLE != None:
        driver.find_element(By.XPATH,'//div[@id="textbox"]').clear()
        driver.find_element(By.XPATH,'//div[@id="textbox"]').send_keys(TITLE)

    driver.find_elements(By.XPATH,'//div[@id="textbox"]')[1].clear()
    driver.find_elements(By.XPATH,'//div[@id="textbox"]')[1].send_keys(description)
    #paper-ripple style-scope ytcp-button
    time.sleep(1)
    try:
        driver.find_element(By.XPATH,'//ytcp-button[@id="toggle-button"]').click()
    except:
        driver.close()
        driver.quit() 
        return False
    time.sleep(1)
    driver.find_element(By.XPATH,'//input[@id="text-input"]').send_keys(tags)
    time.sleep(1)
    driver.find_element(By.XPATH,'//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]').click()
    time.sleep(2)
    driver.find_element(By.XPATH,'//ytcp-button[@id="next-button"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//ytcp-button[@id="next-button"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//ytcp-button[@id="next-button"]').click()
    time.sleep(1)
    #driver.find_element(By.XPATH,'//tp-yt-paper-radio-button[@id="private-radio-button"]').click()
    driver.find_element(By.XPATH,'//tp-yt-paper-radio-button[@name="PUBLIC"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH,'//ytcp-button[@id="done-button"]').click()
    time.sleep(3)
    driver.close()
    driver.quit()  
    return True