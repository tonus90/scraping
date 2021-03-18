import requests
from lxml import html
from pprint import pprint
from urllib.parse import urljoin
import datetime
from pymongo import MongoClient

header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}

url = 'https://yandex.ru/news/'
response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
block_top_news = dom.xpath('//div[@class="mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top"]')[0]
items = block_top_news.xpath('.//article')
print(1)

client = MongoClient('localhost', 27017)
db = client['news']
news_yandex = db['news_yandex']

def save_news(collection):
    news_yandex.insert_one(collection)


def get_datetime(time):
    year = datetime.date.today().year
    month = datetime.date.today().month
    day = datetime.date.today().day
    time = time.split(':')
    hour = int(time[0])
    minute = int(time[1])
    date_res = datetime.datetime(year, month, day, hour=hour, minute=minute)
    return date_res

def name_corrector(name):
    a = name.replace(u'\xa0', ' ')
    print(1)
    return a


for item in items:
    data = {}
    name = item.xpath('.//a/h2/text()')[0]
    url_news = item.xpath('.//a/@href')[0]
    date_time = item.xpath('.//span[@class = "mg-card-source__time"]/text()')[0]
    source = item.xpath('.//span[@class = "mg-card-source__source"]/a/text()')[0]

    data['name'] = name_corrector(name)
    data['url'] = url_news
    data['date'] = get_datetime(date_time)
    data['source'] = source
    print(1)
    save_news(data)







