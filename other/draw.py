import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.

def clickAlert():
  try:
    main_window=driver.current_window_handle
    alert_obj = driver.switch_to.alert
    alert.accept()    
    driver.switch_to.window(main_window)
    time.sleep(5)
    print ("alert accepted")
  except:
    print ("no alert")  

def tryFunction():
  time.sleep(1) # Let the user actually see something!

  clickAlert()

  try:
    form = driver.find_elements_by_class_name('form-detail.hk')
    driver.execute_script("arguments[0].style.display = 'block'; return arguments[0];", form[0])

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

    clickAlert()
  except:
    print ("throw exception")  

  # print (driver.current_url)

  clickAlert()

  curUrl = driver.current_url

  if curUrl == 'https://www.hknycd.com/zh-Hant/system-busy.html':
    driver.back()
    tryFunction()

# driver.get('https://hknycd.com/en/luckydraw-register.html')
driver.get('https://www.hknycd.com/zh-Hant/luckydraw-register.html')
# driver.get('https://hknycd.com/zh-Hant/luckydraw-successful.html')
tryFunction()

time.sleep(5) # Let the user actually see something!
print ('ready')
# driver.quit()

