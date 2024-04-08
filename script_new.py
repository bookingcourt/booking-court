#!/usr/bin/python

# https://stackoverflow.com/questions/70797373/i-want-to-get-orderid-from-api-response-using-selenium-python
# from xvfbwrapper import Xvfb
import sys
import time
import json
import datetime
from datetime import date
import os
import platform
from datetime import date, timedelta
# from colorama import Fore, Back, Style
import requests
import random
import multiprocessing as mp

headers = {
  'Accept': 'application/json',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json; charset=utf-8',
  'Host': 'www.smartplay.lcsd.gov.hk',
  'Pragma': 'no-cache',
  'Referer': 'https://www.smartplay.lcsd.gov.hk/facilities/search-result?keywords=&district=all&startDate=2024-01-06&typeCode=BASC&venueCode=&sportCode=BAGM&typeName=%E7%B1%83%E7%90%83&frmFilterType=&venueSportCode=&isFree=false',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'channel': 'INTERNET',
  'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"'
}

from mongo import checkIsConnected, connectDB, disconnectDB, Venue,\
                  saveDistrict, updateDistrict, saveVenue, updateVenue, saveFa, updateFa, \
                  createSsn, saveSsnToVenue, findVenue, updateSsn, removeOldSsn, getDistByArea, \
                  insertOrUpdateDataInfo, getDataInfoDT
                  # , removeOldDataInfo

# # import base64
# # from selenium import webdriver
# from seleniumwire import webdriver
# # import undetected_chromedriver as webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException 
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.select import Select

# vdisplay = Xvfb()
# vdisplay.start()

# Virtual Display
# from pyvirtualdisplay import Display

# start the virtual display
# display = Display(visible=0, size=(800, 600))
# display.start()

# chrome_options = webdriver.ChromeOptions()
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
# chrome_options.add_experimental_option('useAutomationExtension', False)
# if gHeadless == "Y":
# chrome_options.add_argument('--headless')
# disable gpu will crash in docker container
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--disable-logging')
# chrome_options.add_argument('--disable-software-rasterizer')
# chrome_options.add_argument("--disable-blink-features")
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# prefs = {
#   # 'download.default_directory': download_path,
#   'download.prompt_for_download': False,
#   'download.directory_upgrade': True,
#   'safebrowsing.disable_download_protection': True,
#   "safebrowsing_for_trusted_sources_enabled": False,
#   "safebrowsing.enabled": False,
#   # "dom.webdriver.enabled": False,
#   # 'Page.set_download_behavior': { 'behavior': 'allow', 'downloadPath': download_path }
# }

# prefs = {
#   # 'download.default_directory': download_path,
#   'download.prompt_for_download': True,
#   'download.directory_upgrade': True,
#   'safebrowsing.disable_download_protection': False,
#   "safebrowsing_for_trusted_sources_enabled": True,
#   "safebrowsing.enabled": True,
#   # "dom.webdriver.enabled": False,
#   # 'Page.set_download_behavior': { 'behavior': 'allow', 'downloadPath': download_path }
# }

# chrome_options.add_experimental_option("prefs",prefs)
# courtInfo = []


# driver = webdriver.Chrome(options=chrome_options)

def writeFile(text, path):
  with open(path, "a") as myfile:
    myfile.write(text)

def writeLog(text, suffix=''):
  d = str(date.today()).replace('-', '')
  # d = date.today().weekday()+1
  filename = "./log/{0}{1}.txt".format(d, suffix)
  writeFile(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ": " + text + "\n", filename)

def writeErr(text):
  err = 'Err: {0}'.format(text)
  print (err)
  writeLog(err, "_err")

def deleteLog(suffix=''):
  d = str(date.today() - timedelta(days=gLogKept)).replace('-', '')
  filename = "./log/{0}{1}.txt".format(d, suffix)
  if os.path.exists(filename):
    writeLog('Deleted Log:{}'.format(filename))
    os.remove(filename)

# Create a request interceptor
def interceptor(request):
    del request.headers['Accept-Language']  # Delete the header first
    request.headers['Accept-Language'] = gLang

def getField(data, field):
  if field in data:
    return data[field]
  return None


# def makeRequest(dt, tryCnt):
#   maxTry = 3
#   writeLog("Open web for date {}".format(dt))

#   url = "https://www.smartplay.lcsd.gov.hk/facilities/search-result?keywords=&district=all&startDate={0}&typeCode={1}&venueCode=&sportCode=BAGM&typeName=%E7%B1%83%E7%90%83&frmFilterType=&venueSportCode=&isFree=false".format(dt, gTypeCode)    
#   # writeLog(url)
#   # if gProcessType == "DIST":
#   #   url = "https://www.smartplay.lcsd.gov.hk/rest/param/api/v1/publ/districts/searching-criteria?pgm=N"
#   driver.get(url)
#   # time.sleep(10)
#   # driver.save_screenshot('./log/{}_0.png'.format(dt))
#   try:
#     loadingMask = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".el-loading-mask")))
#     loadingMask = WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.el-loading-mask')))
#     time.sleep(random.randint(2, 5))
#   except TimeoutException:
#     writeLog ('Time out: {}'.format(dt))
#     writeErr ('Time out: {}'.format(dt))
#     driver.save_screenshot('./log/{}.png'.format(dt))
#     if tryCnt < maxTry:
#       tryCnt = tryCnt + 1
#       makeRequest(dt, tryCnt)
#       print('Retry {}: {}'.format(dt, tryCnt))
      
# def visitTheWeb():
#   maxDay = 8 if gProcessType == 'SSN' else 1  
#   print('maxDay:' + str(maxDay), gLang, gTypeCode)
#   driver.request_interceptor = interceptor

#   driver.get("https://www.smartplay.lcsd.gov.hk/home")
#   time.sleep(3)
  
#   for i in range(0, maxDay): #123
#     if i+1 < int(gDtFrom) or i+1 > int(gDtTo):
#       continue
#     dt = date.today() + timedelta(days=i)
#     makeRequest(dt, 0)

def processVenueInfo():
  if checkIsConnected() == False:
    connectDB()  
  venues = Venue.objects()
  for venue in venues:
    # use to get court more info
    url = "https://www.smartplay.lcsd.gov.hk/rest/param/api/v1/publ/venues/{}/info".format(venue["venue_id"])
    # driver.get(url)
    # driver.requests
    data = requests.get(url, headers=headers).json()
    data = data['data']
    oVenue = {
      'venue_id': data['id'],
      'venue_enAddr': data['enAddr'],
      'venue_tcAddr': data['tcAddr'],
      'venue_scAddr': data['scAddr'],
      'venue_phone': data['phone'],
      'venue_lat': getField(data, 'latitude'),
      'venue_long': getField(data, 'longitude'),
      'venue_wkdayHr': '{} - {}'.format(data['weekdayOpenHour'].rjust(4,'0'),data['weekdayCloseHour'].rjust(4,'0')),
      'venue_wkendHr': '{} - {}'.format(data['weekendOpenHour'].rjust(4,'0'),data['weekendCloseHour'].rjust(4,'0'))
    }
    writeLog('[Update Veneu Info] venue_id:{}'.format(oVenue['venue_id']))
    updateVenue(oVenue,True)
  return True

def setFields(obj, srcObj, fields, srcFields):
  for idx, field in enumerate(fields):
    srcField = srcFields[idx]
    if srcField in srcObj:
      obj[field] = srcObj[srcField]
  # return obj

def processDist(areaList):
  for area in areaList:
    # if gArea != 'ALL' and gArea != area['area_code']:
    #   continue
    for dist in area['children']:
      oDist = {}
      setFields(oDist, area, ['area_id', 'area_code', 'area_enName', 'area_tcName', 'area_scName'], ['id', 'code', 'enName', 'tcName', 'scName'])
      setFields(oDist, dist, ['dist_id', 'dist_code', 'dist_enName', 'dist_tcName', 'dist_scName'], ['id', 'code', 'enName', 'tcName', 'scName'])

      if updateDistrict(oDist) == False:
        saveDistrict(oDist)
      # insertOrUpdateDataInfo(gProcessType)
      writeLog('area_code:{} area_code:{} dist_code:{}, dist_name:{}' \
              .format(oDist['area_code'], oDist['area_enName'], oDist['dist_code'], oDist['dist_enName']))

def processResp(data, period):
  jsonPeriod = data[period]
  for dist in jsonPeriod['distList']:
    if not gProcessType in ['dist']:
      processVenueList(dist)
    else:
      print(dist['distCode'], dist['distName'])

def processVenueList(dist):
  for venue in dist['venueList']:
    # if venue['venueId'] != 23:
    #   continue
    oVenue = {  
      'dist_code' : dist['distCode'], 
      'venue_id' : venue['venueId'],
      'venue_imageUrl' : venue['venueImageUrl'],
      'venue_enName' : venue['venueName'] if gLang == 'en' else None,
      'venue_tcName' : venue['venueName'] if gLang == 'zh-hk' else None,
      'venue_scName' : venue['venueName'] if gLang == 'zh-cn' else None,
      'fa_code': gTypeCode
    }    
    if gProcessType in ['FA', 'FAT', 'SSN']:
      processFatList(dist, venue, oVenue) 
    else:
      if updateVenue(oVenue) == False:
        saveVenue(oVenue)
      # insertOrUpdateDataInfo(gProcessType)
      writeLog('venue_id:{} venue_enName:{}' \
              .format(oVenue['venue_id'], oVenue['venue_enName']))
         
def processFatList(dist, venue, oVenue):  
  for fat in venue['fatList']:
    if gProcessType in ('SSN'):
      processSsnList(dist, venue, fat, oVenue)
    else:
      oFa = {
        'fa_id' : fat['fatId'],
        'fa_code' : fat['faCode'],
        'fa_groupCode' : fat['faGroupCode'],
        'fa_enName' : fat['fatName'] if gLang == 'en' else None, 
        'fa_tcName' : fat['fatName'] if gLang == 'zh-hk' else None,
        'fa_scName' : fat['fatName'] if gLang == 'zh-cn' else None
      }    
      if oFa['fa_id'] not in processedFaIds:
        print (processedFaIds, oFa['fa_id'], oFa)
        processedFaIds.append(oFa['fa_id'])
        if updateFa(oFa) == False:
          saveFa(oFa)
        # insertOrUpdateDataInfo(gProcessType)
        writeLog('fa_id:{} fa_enName:{}' \
            .format(oFa['fa_id'], oFa['fa_enName']))

def processSsnList(dist, venue, fat, oVenue): 
  lastVenueId = None
  venueDocu = None
  for ssn in fat['sessionList']:
    if venueDocu == None or lastVenueId == None or lastVenueId != oVenue['venue_id']:      
      venueDocu = findVenue(oVenue)
      if venueDocu == None:
        lastVenueId = None
        print('Venue not found!!!')
        continue
      else:
        lastVenueId = oVenue['venue_id']
              
    ssn_code = fat['faCode'] + "_" +  ssn['ssnStartDate'].replace("-","") + ssn['ssnStartTime'].replace(":", "")
    oSsn = {
      'venue_id': lastVenueId,
      'fa_code': fat['faCode'],
      'ssn_code': ssn_code
    }
    setFields(oSsn, ssn, ['ssn_StartDate', 'ssn_StartTime', 'ssn_EndTime', 'available', 'peak', 'ssn_cnt'], 
                                ['ssnStartDate', 'ssnStartTime', 'ssnEndTime', 'available', 'peak', 'sessionCount'])
    
    updCnt = updateSsn(oSsn)
    if updCnt == 0:
      if oSsn['ssn_cnt'] > 0:
        ssnDocu = createSsn(oSsn)
        saveSsnToVenue(venueDocu, ssnDocu)        
        writeLog('Created venueName:{0} ssn_code:{1} ssn_cnt:{2}'.format(venue['venueName'], ssn_code, oSsn['ssn_cnt']))
    else:
      writeLog('Updated: venueName:{0} ssn_code:{1} ssn_cnt:{2}'.format(venue['venueName'], ssn_code, oSsn['ssn_cnt']))    

def processStart():
  # visitTheWeb()
  maxDay = 8 if gProcessType == 'SSN' else 1  
  periodList = ['morning', 'afternoon', 'evening']
  maxPeriod = 3 if (gProcessType == 'SSN') else 1
  headers["Accept-Language"] = gLang

  p_list = []
  seq = 1

  curTime = (datetime.datetime.now()).strftime('%H')
  if (int(curTime) >= 22):
    startdt = (date.today() + timedelta(days=1))
    if maxDay > 1:
      maxDay = maxDay - 1
  else:
    startdt = date.today()

  # for request in driver.requests:
  #   if request.response:
  for i in range(0, maxDay): #123
    if i+1 < int(gDtFrom) or i+1 > int(gDtTo):
      continue
    dt = startdt + timedelta(days=i)
    if gProcessType == 'DIST':
      url = "https://www.smartplay.lcsd.gov.hk/rest/param/api/v1/publ/districts/searching-criteria?pgm=N"
      writeLog(url)
      data = requests.get(url, headers=headers).json()
      processDist(data['data'])
    else:
      url = 'https://www.smartplay.lcsd.gov.hk/rest/facility-catalog/api/v1/publ/facilities?faCode=BASC&playDate={}'.format(dt)
      writeLog(url)
      data = requests.get(url, headers=headers).json()
      # print(data["data"]["morning"]["distList"][0]["venueList"][0]["fatList"][0]["sessionList"][0]["ssnStartDate"])      
      # data = json.loads(resp.body)
      # writeFile(json.dumps(data, separators=(',', ':')), './json/test.json')
      for periodIndex in range(maxPeriod):
        period = periodList[periodIndex]
        # processResp(data['data'], period)
        p_list.append(mp.Process(target=processResp, args=(data['data'], period)))
        p_list[periodIndex].start()
      for p in p_list:
        p.join()
        p_list = []
      # if gProcessType == 'SSN':
      #   writeLog('data {}, day {} last update date'.format(gProcessType, str(seq)))
      #   insertOrUpdateDataInfo(gProcessType, str(seq))
      #   seq = seq + 1


def withActiveUser(typeCode):
  # exit when no active user in last 1 hour
  lastActiveDT = getDataInfoDT('LAST_ACTIVE_DATETIME_{}'.format(typeCode))  
  if lastActiveDT != None:
    lastActiveMin = round((datetime.datetime.now() - lastActiveDT).total_seconds() / 60.0, 2)
  if lastActiveDT == None or lastActiveMin > 60:   
    err = 'No active user'
    if lastActiveDT != None:
      err = '{} since {} mins ago.'.format(err, lastActiveMin)
    print(err)
    writeLog(err)
    sys.exit()

def tooOftenUpdate(info_type, mins):
  lastUpdateDt = getDataInfoDT(info_type)
  if lastUpdateDt != None:
    lastUpdateMin = round((datetime.datetime.now() - lastUpdateDt).total_seconds() / 60.0, 2)
    if lastUpdateMin <= mins:
      err = 'Updated within {} mins.'.format(lastUpdateMin)
      print(err)
      writeLog(err)
      sys.exit()

gLogKept = 7
gProcessType = "DIST" if len(sys.argv) < 2 else sys.argv[1]     # DIST, VENUE, VENUE_INFO, FA, SSN, RM_OLD
gTypeCode = "BASC" if len(sys.argv) < 3 else sys.argv[2]        # BASC, BADC, VOLC
gLang = "en" if len(sys.argv) < 4 else sys.argv[3]              # en / zh-hk / zh-cn
gArea = 'ALL' if len(sys.argv) < 5 else sys.argv[4]             # HK / KLN / NTE / NTW  
gDtRange = '1-8' if len(sys.argv) < 6 else sys.argv[5]          # 1-2, 1-8
gDtFrom = gDtRange.split('-')[0]
gDtTo = gDtRange.split('-')[1]
gDistList = []
processedFaIds = []

if __name__ == '__main__':
  try:
    if gArea != 'ALL':
      coll = getDistByArea(gArea)
      for item in coll:
        gDistList.append(item.dist_code)

    print (gProcessType, gTypeCode, gLang, gArea, gDistList, gDtRange)
    startdt = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    
    print("Started {0}".format(startdt))
    writeLog ("Start {0}".format(startdt).center(100, "#"))
    
    
    if gProcessType == 'RM_OLD':
      writeLog("start remove old session")
      cnt = removeOldSsn(gTypeCode)
      # removeOldDataInfo('SSN')
      deleteLog()
      deleteLog('_err')
      writeLog("end remove old record. Count: {0}".format(str(cnt)))
    elif gProcessType == 'VENUE_INFO':
      processVenueInfo()
    else:
      if gProcessType == 'SSN':
        withActiveUser(gTypeCode)
        # Update again within 15 minutes then exit
        # tooOftenUpdate(gProcessType + '_' + gTypeCode, 15)

      writeLog("start processing {},{},{},{},{},{}".format(gProcessType, gTypeCode, gLang, gArea, gDistList, gDtRange))
      processStart()
      writeLog("end processing")

      if gProcessType == 'SSN':
        insertOrUpdateDataInfo(gProcessType + '_' + gTypeCode)
    enddt = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    writeLog ("Done {0} - {1}".format(startdt, enddt).center(100, "#"))
    print("Finished {0}".format(enddt))
  except Exception as error:  
    writeErr(error)
    raise 
  # finally:    
    # vdisplay.stop()
    # driver.quit()
    


  # print (courtInfo)
  # driver.close()

  # url to get district 
  # https://www.smartplay.lcsd.gov.hk/rest/param/api/v1/publ/districts/searching-criteria?pgm=N