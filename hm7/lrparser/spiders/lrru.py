import scrapy
from scrapy.http import HtmlResponse

from lrparser.items import LrparserItem
from scrapy.loader import ItemLoader

class LrruSpider(scrapy.Spider):
    name = 'lrru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, query):
        super(LrruSpider, self).__init__()
        self.query = query
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']
        
    def take_name(self):
        return self.query

    def parse(self, response):
        goods_urls = response.xpath('//uc-product-list/product-card//a[@slot="name"]/@href')
        for link in goods_urls:
            yield response.follow(link, callback=self.good_parse)
        next_page = response.xpath('//div[@class="next-paginator-button-wrapper"]//@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def good_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LrparserItem(), response=response)
        loader.add_xpath('name', '//h1//text()')
        loader.add_xpath('photos', '//uc-pdp-media-carousel/img[@slot="thumbs"]/@src')
        loader.add_xpath('price', '//meta[@itemprop="price"]/@content')
        loader.add_xpath('property', '//dl/div/dt/text()')
        loader.add_xpath('property_val', '//dl/div/dd/text()')
        # loader.add_css()
        loader.add_value('url', response.url)
        yield loader.load_item()
