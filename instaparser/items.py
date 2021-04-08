# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()
    flwr_login_name = scrapy.Field()
    name = scrapy.Field()
    flwr_id = scrapy.Field()
    user_data = scrapy.Field()
    hash = scrapy.Field()
    is_follower = scrapy.Field()
    is_following = scrapy.Field()
    _id = scrapy.Field()