import requests
from lxml import html
from pprint import pprint
from urllib.parse import urljoin
import datetime
from pymongo import MongoClient

header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}

url = 'https://lenta.ru/'
response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
items = dom.xpath('//div[@class="span4"]/div[@class="item"] | //div[@class="first-item"]')

client = MongoClient('localhost', 27017)
db = client['news']
news_lenta = db['news_lenta']

def save_news(collection):
    news_lenta.insert_one(collection)


def get_datetime(list_with_date):
    year = datetime.date.today().year  # получим год на всякий
    months = {
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'май': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'ноя': 11,
        'дек': 12,
    }

    for i in list_with_date[0].split(','):
        if i.find(':') != -1:
            time = i.split(':')
            hour = int(time[0])
            minute = int(time[1])
        else:
            date = i.split(' ')
            day = int(date[1])
            month = int(months[date[2][:3:]])
            year = int(date[3])

    date_res = datetime.datetime(year, month, day, hour=hour, minute=minute)
    return date_res

def name_corrector(name):
    a = name.replace(u'\xa0', ' ')
    print(1)
    return a


for item in items:
    data = {}
    if item.attrib['class'] == 'first-item':
        name = item.xpath('.//text()')[1]
        url_news = urljoin(url, item.xpath('./a/@href')[0])
        date_time = item.xpath('.//a/time/@datetime')
        source = 'https://lenta.ru/'
    else:
        name = item.xpath('.//text()')[1]
        url_news = urljoin(url, item.xpath('./a/@href')[0])
        date_time = item.xpath('.//a/time/@datetime')
        source = 'https://lenta.ru/'

    data['name'] = name_corrector(name)
    data['url'] = url_news
    data['date'] = get_datetime(date_time)
    data['source'] = source
    print(1)
    save_news(data)







