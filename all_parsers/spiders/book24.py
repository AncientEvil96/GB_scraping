# II вариант
# 1) Создать двух пауков по сбору данных о книгах с сайтов labirint.ru и book24.ru
# 2) Каждый паук должен собирать:
# * Ссылку на книгу
# * Наименование книги
# * Автор(ы)
# * Основную цену
# * Цену со скидкой
# * Рейтинг книги
# 3) Собранная информация дожна складываться в базу данных
# (Нужно ли здесь обновление? Нужны ли дубликаты?)

import scrapy
from scrapy.http import HtmlResponse
from all_parsers.items import AllParsersItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/novie-knigi/']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//div[contains(@class, "product-list__item")]'
                               '//div[contains(@class, "product-card__content")]'
                               '//a[contains(@class, "product-card__name smartLink")]/@href').getall()
        for link in links:
            yield response.follow(link, self.process_item)

        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page:
            print(next_page)
            yield response.follow(next_page, self.parse)

    def process_item(self, response: HtmlResponse):
        info = AllParsersItem()
        info['href'] = response.url
        info['name'] = response.xpath('//h1/text()').get()
        info['autor'] = response.xpath('//a[@itemprop="author"]/text()').get()
        info['price'] = response.xpath('//b[@itemprop="price"]/text()').get()
        info['discount'] = response.xpath('//div[contains(@class,"item-actions__price-old")]/text()').get()
        info['rate'] = response.xpath('//span[@itemprop="ratingValue"]/text()').get()
        info['id'] = response.xpath('//a/@data-product').get()
        yield info
