# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import scrapy
from pymongo import MongoClient


class AllParsersPipeline:
    def __init__(self):
        self.client = MongoClient('localhost:27017')
        self.db = self.client['books_stores']

    def process_item(self, item, spider: scrapy.Spider):
        if spider.name == 'labirint':
            item['price'] = float(item['price']) if item['price'] else 0
            item['discount'] = float(item['discount']) if item['discount'] else 0
            item['rate'] = float(item['rate'])
            item['id'] = int(item['href'].split('/')[-2])
        else:
            if item['discount']:
                item['discount'], item['price'] = item['price'], item['discount']

            item['price'] = float(item['price'].strip().replace('р.', '')) if item['price'] else 0
            item['discount'] = float(item['discount'].strip().replace('р.', '')) if item['discount'] else 0
            item['rate'] = float(item['rate'].strip().replace(',', '.'))
            item['id'] = int(item['id'])
        self.db[spider.name].update_one({'id': {'$eq': item['id']}}, {'$set': item}, upsert=True)
        return item

    def close_spider(self):
        self.client.close()
