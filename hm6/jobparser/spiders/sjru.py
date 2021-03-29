import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
from urllib.parse import urljoin

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response):
        base = 'https://www.superjob.ru/'
        urls = [urljoin(base, url) for url in response.xpath("//div[@class='jNMYr GPKTZ _1tH7S']/div/a/@href").extract()]
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)
        next_page = urljoin(base, response.xpath("//a[@class='icMQ_ bs_sM _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first())
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        vacancy_name = response.xpath("//h1//text()").extract_first()
        vacancy_salary = response.xpath("//span[@class='_3mfro _2Wp8I PlM3e _2JVkc']/text()").extract()
        vacancy_url = response.url
        yield JobparserItem(name=vacancy_name, salary=vacancy_salary, url=vacancy_url)
        print(1)