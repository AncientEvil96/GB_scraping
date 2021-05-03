# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


class LeroyParserItem(scrapy.Item):

    @staticmethod
    def get_big_img(url: str):
        return url.replace('w_82,h_82', 'w_2000,h_2000')

    @staticmethod
    def get_property(property_list):
        key, value = property_list
        return {key.strip(): value.strip()}

    _id = scrapy.Field()
    id = scrapy.Field(output_processor=TakeFirst())
    href = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    key = scrapy.Field()
    value = scrapy.Field()

    property = scrapy.Field(input_processor=MapCompose(get_property))
    img = scrapy.Field(input_processor=MapCompose(get_big_img))
