# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LeroyParserItem(scrapy.Item):
    # _id = scrapy.Field()
    # id = scrapy.Field()
    href = scrapy.Field()
    name = scrapy.Field()
    # autor = scrapy.Field()
    price = scrapy.Field()
    # discount = scrapy.Field()
    # rate = scrapy.Field()

    pass
