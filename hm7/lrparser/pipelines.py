# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
import hashlib
from scrapy.utils.python import to_bytes
from scrapy.http import HtmlResponse

class LrparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['lerua']

    def process_item(self, item, spider):

        item['properties'] = self._get_properties(item['property'], item['property_val'])
        del item['property']
        del item['property_val']
        collection = self.db[spider.take_name()]
        collection.insert_one(item)

        return item

    def _get_properties(self, props, values):
        data= {}
        for prop in props:
            index = props.index(prop)
            data[prop]=self._get_value(values)[index]
        return data

    def _get_value(self, values):
        my_list = []
        for val in values:
            my_list.append(val.split()[0])
        return my_list

class LrphotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{item["name"][0]}/{image_guid}.jpg'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

