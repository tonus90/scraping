from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from urllib.parse import urljoin
import requests
from pymongo import MongoClient

login = 'study.ai_172'
password = 'NextPassword172'

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://mail.ru/')
time.sleep(1)
elem = driver.find_element_by_class_name('email-input')
elem.send_keys(login)
elem.send_keys(Keys.ENTER)
time.sleep(0.5)
elem = driver.find_element_by_class_name('password-input')
elem.send_keys(password)
elem.send_keys(Keys.ENTER)
urls = set()
time.sleep(3)
mails = [1,2]

while True:
    old_mails = mails
    mails = driver.find_elements_by_class_name('llc')
    if old_mails[-1] == mails[-1]:
        break
    for j in mails:
        href = (j.get_property('href'))
        urls.add(href)
    actions = ActionChains(driver)
    actions.move_to_element(mails[-1])
    actions.perform()
print(1)

client = MongoClient('localhost', 27017)
db = client['mailru']
mails = db['mails']
data = {}

for i in urls:
    driver.get(i)
    time.sleep(2)
    name = driver.find_element_by_xpath('//div[@class="letter__author"]/span')
    data['name'] = name.text
    data['email'] = name.get_property('title')
    data['date'] = driver.find_element_by_xpath('//div[@class="letter__date"]').text
    data['theme'] = driver.find_element_by_xpath('//h2').text
    data['text'] = driver.find_element_by_xpath('//div[@class="letter-body"]').text
    mails.insert_one(data)
    data = {}

