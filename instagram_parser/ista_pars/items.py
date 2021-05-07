# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Compose
import logging

logging.basicConfig(filename="log_items.log", level=logging.INFO)


def get_dict(self):
    return {'following': [], 'followers': []}


def get_clean_data(line: dict):
    node = line['node']
    try:
        img = node['profile_pic_url']
    except ValueError as err:
        logging.error(err)
        img = None

    try:
        data_info = {
            'id': node['id'],
            'name': node['full_name']
        }
    except ValueError as err:
        logging.error(err)
        data_info = None

    my_tuple = zip([data_info], [img])

    # TODO: был вариант вида:
    # my_tuple = (data_info, img)
    # но почему то не формировался кортеж

    return my_tuple

class IstaParsItem(scrapy.Item):
    _id = scrapy.Field()
    id = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    # TODO: почему то не работает, хотел сделать пустой словарик и потом его в pipeline заполнить
    # пришлось сделать в пауке
    # user_data = scrapy.Field(input_processor=Compose(get_dict))
    user_data = scrapy.Field(output_processor=TakeFirst())
    data_type = scrapy.Field(output_processor=TakeFirst())
    # info = scrapy.Field()
    info = scrapy.Field(input_processor=MapCompose(get_clean_data))
