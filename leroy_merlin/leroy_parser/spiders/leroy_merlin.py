# Перед работой над заданием
# Посмотрите комментарий об item_completed - https://gb.ru/lessons/124840#!#comment-725664
#
# Замечания
# Цена => преобразовать в число
# Параметры(характеристики товара) => придумать как их хранить в одном поле Item'а
#
# Задание
# 1) Взять любую категорию товаров на сайте Леруа Мерлен(еще лучше - использовать input и конструктор паука).
# Собрать с использованием ItemLoader следующие данные:
# ● название;
# ● все фото;
# ● параметры товара в объявлении(не часть HTML!);
# ● ссылка;
# ● цена.
#
# С использованием output_processor и input_processor реализовать очистку и преобразование данных.
# Цены должны быть в виде числового значения.
#
# С сохранением в MongoDB!
# Без дубликатов!
#
# 2)Написать универсальный обработчик характеристик товаров, который будет формировать данные вне
# зависимости от их типа и количества.
#
# 3)Реализовать хранение скачиваемых файлов в отдельных папках, каждая из которых должна
# соответствовать собираемому товару

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from leroy_merlin.leroy_parser.items import LeroyParserItem


class LeroyMerlinSpider(scrapy.Spider):
    name = 'leroy_merlin'
    allowed_domains = ['naberezhnye-chelny.leroymerlin.ru']

    def __init__(self, search: str):
        super().__init__()
        self.start_urls = [f'https://naberezhnye-chelny.leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[@class="phytpj4_plp largeCard"]//a[@data-qa="product-name"]/@href')
        for link in links:
            yield response.follow(link, self.process_item)

        next_page = response.xpath('//a[contains(@aria-label,"Следующая страница")]/@href')
        if next_page:
            yield response.follow(next_page, self.parse)

    def process_item(self, response: HtmlResponse):
        item = LeroyParserItem()
        loader = ItemLoader(item=item, response=response)
        loader.add_xpath('id', '//@context-id')
        loader.add_value('href', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('key', '//dt[@class="def-list__term"]/text()')
        loader.add_xpath('value', '//dd[@class="def-list__definition"]/text()')
        loader.add_xpath('img', '//img[contains(@slot,"thumbs")]/@src')

        yield loader.load_item()