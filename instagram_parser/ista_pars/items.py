# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose


def get_clean_data(line: dict):
    node = line['node']
    try:
        img = node['profile_pic_url']
    except ValueError as err:
        print(err)
    else:
        img = None

    try:
        data_info = {
            'id': node['id'],
            'name': node['full_name']
        }
    except ValueError as err:
        print(err)
    else:
        data_info = None

    return (data_info, img)


class IstaParsItem(scrapy.Item):
    _id = scrapy.Field()
    user_id = scrapy.Field()
    name = scrapy.Field()
    edges = scrapy.Field(input_processor=MapCompose(get_clean_data))
    id_parent = scrapy.Field(output_processor=TakeFirst())
    data_type = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
