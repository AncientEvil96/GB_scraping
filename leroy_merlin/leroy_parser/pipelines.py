# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from pymongo import MongoClient



class LeroyParserPipeline:

    def __init__(self):
        self.client = MongoClient('localhost:27017')
        self.db = self.client['leroy_assortiments']

    def process_item(self, item, spider: scrapy.Spider):
        item['property'] = self.get_property(list(zip(item['key'], item['value'])))
        item['img'] = self.get_big_img(item['img'])
        # self.db[spider.name].update_one({'id': {'$eq': item['id']}}, {'$set': item}, upsert=True)
        return item

    def get_property(self, property_list: list):
        return [{key.strip(): value.strip()} for key, value in property_list]

    def close_spider(self):
        self.client.close()

    # def get_extension(self, headers):
    #     if 'Content-Type' not in headers:
    #         raise ValueError('Not need headers parametrs')
    #     return headers['Content-Type'].split('/')[-1]
