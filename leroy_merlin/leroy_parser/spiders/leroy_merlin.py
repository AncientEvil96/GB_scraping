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
from leroy_merlin.leroy_parser.items import LeroyParserItem


class LeroyMerlinSpider(scrapy.Spider):
    name = 'leroy_merlin'
    allowed_domains = ['naberezhnye-chelny.leroymerlin.ru']
    start_urls = ['https://naberezhnye-chelny.leroymerlin.ru/catalogue/elektroinstrumenty/']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[@class="phytpj4_plp largeCard"]//a[@data-qa="product-name"]/@href').getall()
        for link in links:
            yield response.follow(link, self.process_item)

        next_page = response.xpath('//a[contains(@aria-label,"Следующая страница")]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def process_item(self, response: HtmlResponse):
        info = LeroyParserItem()
        info['href'] = response.url
        info['name'] = response.xpath('//h1/text()').get()
        # info['autor'] = response.xpath('//div[@class="authors"]/a/text()').get()
        info['price'] = response.xpath('//span[@slot="price"]/text()').get()
        # info['discount'] = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        # info['rate'] = response.xpath('//div[@id="rate"]/text()').get()
        yield info
