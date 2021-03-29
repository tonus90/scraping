from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.mvideo.ru/'
driver.get(url)
time.sleep(1)
block_hit = driver.find_element_by_xpath('//div[@class="gallery-title-wrapper"]/div[contains(text(),"Хиты продаж")][1]/../../..')

urls = set()
while True:
    button = block_hit.find_element_by_class_name('next-btn')
    hits_test = block_hit.find_elements_by_tag_name('li')
    button.click()
    time.sleep(2)
    hits = block_hit.find_elements_by_tag_name('li')
    if len(hits_test) < len(hits):
        button.click()
        hits = block_hit.find_elements_by_tag_name('li')
    else:
        for i in hits:
            a = i.find_element_by_tag_name('a')
            href = a.get_property('href')
            urls.add(href)
        break

client = MongoClient('localhost', 27017)
db = client['mvideo']
hits_coll = db['hits']
data = {}

for i in urls:
    driver.get(i)
    time.sleep(2)
    data['name'] = driver.find_element_by_tag_name('h1').text
    data['price'] = driver.find_element_by_class_name('fl-pdp-price__current').text
    data['count_reviews'] = float(driver.find_element_by_class_name('c-star-rating_reviews-qty').text)
    hits_coll.insert_one(data)
    data = {}
