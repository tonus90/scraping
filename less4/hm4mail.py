import requests
from lxml import html
from pprint import pprint
from urllib.parse import urljoin
import datetime
from pymongo import MongoClient

header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}

url = 'https://news.mail.ru/'
response = requests.get(url, headers=header)

dom = html.fromstring(response.text)
block_news = dom.xpath('//li[@class="list__item"]/a[@class = "list__text"]/@href')


client = MongoClient('localhost', 27017)
db = client['news']
news_mail = db['news_mail']

def save_news(collection):
    news_mail.insert_one(collection)

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

for url_news in block_news:
    response_news = requests.get(url_news, headers=header)
    dom_news = html.fromstring(response_news.text)
    data = {}
    name = dom_news.xpath('.//h1/text()')[0]
    date_time = dom_news.xpath('.//span[@class="note"]//@datetime')[0]
    # date = datetime.datetime.strptime(date_time, '%Y%m%d').date()
    """
    Вот тут вопросик, сюда по сути дата попадает в нужном формате в таком виде: "2021-03-18T15:49:19+03:00", но
    тип данных сринг, как можно быстро преобразовать такую строку в datetime не распарсивая, не разбивая ее, не прогоняя ее через какую-то самописную функцию
    """
    source = dom_news.xpath('.//span[@class="note"]//span[@class="link__text"]/text()')[0]

    data['name'] = name_corrector(name)
    data['url'] = url_news
    data['date'] = date_time
    data['source'] = source
    save_news(data)







