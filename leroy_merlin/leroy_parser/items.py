# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def get_big_img(url: str):
    return url.replace('w_82,h_82', 'w_2000,h_2000')


def get_property(property_line):
    key, value = property_line
    return {key.strip(): value.strip()}


def get_strip(value):
    return value.strip()


def get_int(value):
    return int(value[0].strip().replace(' ', ''))


class LeroyParserItem(scrapy.Item):
    # @staticmethod
    # def get_big_img(url: str):
    #     return url.replace('w_82,h_82', 'w_2000,h_2000')

    # @staticmethod
    # def get_property(property_list):
    #     key, value = property_list
    #     return {key.strip(): value.strip()}

    _id = scrapy.Field()
    id = scrapy.Field(output_processor=TakeFirst())
    href = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=Compose(get_int))
    key = scrapy.Field(input_processor=MapCompose(get_strip))
    value = scrapy.Field(input_processor=MapCompose(get_strip))
    property = scrapy.Field(input_processor=MapCompose(get_property))
    img = scrapy.Field(input_processor=MapCompose(get_big_img))
    print()
