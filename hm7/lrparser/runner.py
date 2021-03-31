from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lrparser import settings
from lrparser.spiders.lrru import LrruSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule('settings')

    process = CrawlerProcess(settings=crawler_settings)
    query = input('Ввести товар:')
    abc = query
    process.crawl(LrruSpider, query=query) #[MSI, Gigabyte]

    process.start()
