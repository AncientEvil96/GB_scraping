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


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%A2%D0%B0%D1%80%D0%BC%D0%B0%D1%88%D0%B5%D0%B2/?stype=0']

    def parse(self, response: HtmlResponse):
        info_list = []

        links = response.xpath('//div[contains(@class,"card-column")]//a[@class="product-title-link"]/@href').getall()
        for link in links:
            yield response.follow(link, self.process_item)

        next_page = response.xpath('//div[@class="pagination-next"]/a/@href').get()
        if next_page:
            print(next_page)
            yield response.follow(next_page, self.parse)

    def process_item(self, response: HtmlResponse):
        info = AllParsersItem()
        info['href'] = response.url
        info['name'] = response.xpath('//div[@id="product-title"]/h1/text()').get()
        info['autor'] = response.xpath('//div[@class="authors"]/a/text()').get()
        info['price'] = response.xpath('//div[contains(@class,"buying-price")]'
                                       '//span[contains(@class,"-number")]/text()').get()
        info['discount'] = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        info['rate'] = response.xpath('//div[@id="rate"]/text()').get()
        yield info
