import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?area=&fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response):
        urls = response.xpath("//a[@data-qa ='vacancy-serp__vacancy-title']/@href").extract()
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)
        next_page = response.css("a.HH-Pager-Controls-Next::attr('href')").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        vacancy_name = response.xpath("//h1//text()").extract_first()
        vacancy_salary = response.xpath("//p[@class='vacancy-salary']/span/text()").extract()
        vacancy_url = response.url
        yield JobparserItem(name=vacancy_name, salary=vacancy_salary, url=vacancy_url)
        print(1)