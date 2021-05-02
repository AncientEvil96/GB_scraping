# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose
from abc import ABC, abstractmethod


class LeroyParserItem(scrapy.Item):
    _id = scrapy.Field()
    id = scrapy.Field(output_processor=TakeFirst())
    href = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    key = scrapy.Field()
    value = scrapy.Field()
    property = scrapy.Field()
    img = scrapy.Field(input_processor=MapCompose())

    @abstractmethod
    def get_big_img(self, img: list):
        return [i.replace('w_82,h_82', 'w_2000,h_2000') for i in img]


LeroyParserItem.get_big_img()