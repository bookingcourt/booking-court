import json
import requests
from datetime import date
from datetime import date, timedelta


# solution found in https://stackoverflow.com/questions/68895582/how-to-avoid-a-bot-detection-and-scrape-a-website-using-python
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


url = "https://www.smartplay.lcsd.gov.hk/rest/param/api/v1/publ/venues/{}/info".format(209)
response = requests.get(url, headers=headers).json()
print(response)


for i in range(0, 8): #123
  dt = date.today() + timedelta(days=i)
  response = requests.get(
      'https://www.smartplay.lcsd.gov.hk/rest/facility-catalog/api/v1/publ/facilities?faCode=BASC&playDate={}'.format(dt), 
      headers=headers).json()
  # you should parse items here.
  print(response["data"]["morning"]["distList"][0]["venueList"][0]["fatList"][0]["sessionList"][0]["ssnStartDate"])
  print("\n")


# if not response["items"]:
#     break
# data_dict = json.loads(data)
# data_dict["pagination"]["page"] = data_dict["pagination"]["page"]+1 # get the next page.
# data = json.dumps(data_dict)