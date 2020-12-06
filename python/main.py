# by Itai Guli

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import pyperclip
import time

with open('cities.json', encoding='utf-8-sig') as cities_json:
    cities = cities_json.read()
    cities = json.loads(cities)

driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
driver.get('https://web.whatsapp.com/')
input("Scan QR and press any button to start the script: ") # waiting for user action.

all_groups = ["NameGroup4","NameGroup3","NameGroup2","NamGroup1"] # The Name of the Groups
last_areas = [] # all last areas for filter

def send_whatsapp(areas_for_sending):

    if len(last_areas) <= 0:
        title = "*צבע אדום - התרעות פיקוד העורף:*"
    else:
        title = ""

    whatsapp_message = ""
    for zone in areas_for_sending:
        whatsapp_message = whatsapp_message + ("*• אזור " + zone + ":* ") + ', '.join(areas_for_sending[zone]['areas']) + "\n"

    message = title + "\n" + time.strftime("%d/%m/%Y %H:%M:%S:") + "\n" + whatsapp_message

    time.sleep(0.1)
    pyperclip.copy(message)

    for groupName in all_groups:
        try:
            time.sleep(0.1)
            user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(groupName)) # chat name by xpath
            time.sleep(0.1)
            user.click()
            ActionChains(driver).key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform()
            time.sleep(0.1)
            ActionChains(driver).send_keys(u'\ue007').perform() # press ENTER
        except:
            pass


def format_list(list_areas):
  areas_for_sending = {}
  for cityValue in list_areas:
    for i in cities:
      if i['value'] == cityValue:  # find in the json city file
        cityName = i['name']
        zone = i['zone']  # zone of alert area

        if zone not in areas_for_sending:
          areas_for_sending[zone] = {"areas": [cityName]}
        else:
          areas_for_sending[zone]['areas'].append(cityName)
        break # break 'for-loop'
    else:
      areas_for_sending[cityValue] = {"areas": [cityValue]}
   
while True:
  try:
    time.sleep(1) # a delay
    response = requests.get("https://www.oref.org.il/WarningMessages/alert/alerts.json", headers={'X-Requested-With': 'XMLHttpRequest', 'Referer': 'https://www.oref.org.il/'}) # important to add headers
       
    if len(response.content) < 5 or "{" not in response.text or "בדיקה" in response.text:
      if len(last_areas) > 0:
        last_areas = []  # set default when alert finished
      continue
    
    list_oref = json.loads((response.content).decode('utf8'))["data"]
    filtered_areas = list({area for (area) in (list_oref) if (area not in last_areas) or (list_oref.count(area) > 1 and last_areas.count(area) == 1)})
    filtered_areas.sort()

    last_areas = list(list_oref)
       
    if len(filtered_areas) > 0:
      try:
        send_whatsapp(format_list(filtered_areas))
      except Exception as e:
        print(e)
        pass
           
  except Exception as e:
    print(e)
    pass
