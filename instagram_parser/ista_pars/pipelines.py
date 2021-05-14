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
import logging

logging.basicConfig(filename='log_pipelines.log', level=logging.INFO)


class InstImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['info'][1]:
            try:
                yield scrapy.Request(item['info'][1])
            except Exception as err:
                logging.error(err)

    def item_completed(self, results, item, info):
        if results:
            item['info'][1]['img'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'img/{item["info"][0]["id"]}/{image_guid}.jpg'


class IstaParsPipeline:

    def __init__(self):
        self.client = MongoClient('localhost:27017')
        self.db = self.client['instagram']
        self.db_name = 'user_info'

    def process_item(self, item, spider: scrapy.Spider):
        list_ = item['user_data'].get(item['data_type'])
        data_type = item['data_type']
        item['user_data'].update({data_type: list_ + self.get_list_info(item['info'])})
        del item['data_type']
        del item['info']

        collection = self.db[self.db_name]
        result = collection.find({'_id': {'$eq': item['id']}})

        # TODO: хз почему не работают конструкции типа len(list(result)) или [i for i in result]
        first_recording = True
        for line in result:
            first_recording = False
            break

        if first_recording:
            collection.update_one({'_id': {'$eq': item['id']}}, {'$set': item}, upsert=True)
        else:
            for line in item['user_data'][data_type]:
                collection.update_one({'_id': {'$eq': item['id']}},
                                      {'$addToSet': {f'user_data.{data_type}': line}},
                                      upsert=True
                                      )
        return item

    def get_list_info(self, list_info: list):
        return [i[0] for i in list_info]

    def close_spider(self):
        self.client.close()
