# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
from pathlib import Path

class InstaparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['instagram']

    def process_item(self, item, spider):
        name = item['username']
        del item['username']
        if item['hash']== '5aefa9893005572d237da5068082d8d5':
            item['is_follower'] = True
            item['is_following'] = False
        elif item['hash']== '3dec7e2c57367ef3da3d987d89f9dbc8':
            item['is_follower'] = False
            item['is_following'] = True
        # del item['hash']
        collection = self.db[name]
        collection.insert_one(item)
        return item


class InstphotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            try:
                yield scrapy.Request(item['photo'])
            except Exception as e:
                print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{item["username"]}/{item["name"]}.jpg'

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item