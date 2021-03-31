# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst

def process_url(value):
    if value:
        value = value.replace('82', '2000')
    return value

def process_price(price):
    if price:
        price = float(''.join(price.split()))
    return price


class LrparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_url))
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    property = scrapy.Field()
    property_val = scrapy.Field()
    properties = scrapy.Field()
    _id = scrapy.Field()
