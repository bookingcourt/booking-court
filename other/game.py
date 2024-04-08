import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.

def tryFunction():
  time.sleep(1) # Let the user actually see something!
  # regBtn = driver.find_elements_by_class_name('hk.button.purple')

  form = driver.find_elements_by_class_name('form-detail.hk')

  driver.execute_script("arguments[0].style.display = 'block'; return arguments[0];", form[0])

  # print (form[0])

  email = driver.find_element_by_id('login-contact')
  val = email.get_attribute('value')
  if val == "":
    email.send_keys('ccm1130@gmail.com')
  hkid = driver.find_element_by_id('login-code')
  val = hkid.get_attribute('value')
  if val == "":
    hkid.send_keys('Z5448')
  regBtn = driver.find_element_by_id('login-button')
  regBtn.click()

  time.sleep(5)

  # print (driver.current_url)

  curUrl = driver.current_url

  print (curUrl)
  if curUrl == 'https://www.hknycd.com/zh-Hant/system-busy.html':
    # time.sleep(5)
    driver.back()
    tryFunction()

# driver.get('https://hknycd.com/en/luckydraw-register.html')
driver.get('https://www.hknycd.com/zh-Hant/card-game-register.html')
tryFunction()

time.sleep(5) # Let the user actually see something!
# driver.quit()
print ('ready')

