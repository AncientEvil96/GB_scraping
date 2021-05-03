from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroy_parser import settings
from leroy_parser.spiders.leroy_merlin import LeroyMerlinSpider
from urllib.parse import quote_plus

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    text_s = input('Write search text: ')
    search = quote_plus(text_s)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyMerlinSpider, search=search)
    process.start()