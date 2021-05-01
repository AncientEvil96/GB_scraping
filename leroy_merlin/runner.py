from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroy_parser import settings
from leroy_parser.spiders import leroy_merlin

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)

    process.crawl(leroy_merlin)

    process.start()