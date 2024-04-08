import sys
import time
import json
import datetime
from datetime import date
import os
import platform
from datetime import date, timedelta
# from colorama import Fore, Back, Style
# import requests

# import base64
# from selenium import webdriver
from seleniumwire import webdriver
# import undetected_chromedriver as webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-notifications")
# chrome_options.add_argument('--verbose')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument("--disable-setuid-sandbox")
# chrome_options.add_argument('--window-size=800,600')
# chrome_options.add_argument('--disable-plugins-discovery')
# # chrome_options.add_argument('--disable-extensions')
# # chrome_options.add_argument('--profile-directory=Default')
# chrome_options.add_argument('--incognito')
# # chrome_options.add_argument('--start-maximized')
# # to set navigator.webdriver to undefined
# chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument('--headless')

print('started')
driver = webdriver.Chrome(options=chrome_options)
dt = date.today()
# url = "https://www.smartplay.lcsd.gov.hk/facilities/search-result?keywords=&district=all&startDate={0}&typeCode=BASC&venueCode=&sportCode=BAGM&typeName=%E7%B1%83%E7%90%83&frmFilterType=&venueSportCode=&isFree=false".format(dt)
url = "https://www.smartplay.lcsd.gov.hk/facilities/select/court?venueId=23&fatId=22&venueName=%E6%9E%97%E5%A3%AB%E5%BE%B7%E9%AB%94%E8%82%B2%E9%A4%A8&sessionIndex=0&dateIndex=0&playDate=2023-12-24&district=KWT&typeCode=BADC&typeName=%E7%BE%BD%E6%AF%9B%E7%90%83&keywords=&sportCode=BAGM&frmFilterType=&isFree=false"
print (url)
driver.get(url)

eachCrtBtn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.sp-tabs-item.sp-tabs-item-op.sp-tabs-item-op1")))
ActionChains(driver).move_to_element(eachCrtBtn).click().perform()
# loadingMask = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".el-loading-mask")))
# loadingMask = WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.el-loading-mask')))
time.sleep(2)
# driver.get_screenshot_as_file("./screenshot.png")
for request in driver.requests:
  if request.response:
    if "1?playDate=" in request.url and "/api/" in request.url:
      resp = request.response     
      data = json.loads(resp.body)
      print(data['data']['frmList'])
      print(request.url)
      # print(request.response.status_code)
input ('press to exit')
driver.quit()
print('finished')