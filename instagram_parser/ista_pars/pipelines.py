# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from pymongo import MongoClient
import hashlib
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class InstImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['edges'][1]:
            try:
                yield scrapy.Request(item['edges'][1])
            except Exception as err:
                print(err)

    def item_completed(self, results, item, info):
        if results:
            item["img"] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'full/{item["edges"][0]["id"]}/{image_guid}.jpg'



class IstaParsPipeline:

    def __init__(self):
        self.client = MongoClient('localhost:27017')
        self.db = self.client['leroy_assortiments']

    def process_item(self, item, spider):
        info = item['edges'][0]
        item['user_id'] = info['id']
        item['name'] = info['name']
        del item['edges']
        self.db[spider.name].update_one({'id': {'$eq': item['id']}}, {'$set': item}, upsert=True)
        return item
        return item

    def close_spider(self):
        self.client.close()
