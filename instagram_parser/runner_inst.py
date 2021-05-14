from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from instagram_parser.ista_pars.spiders.instagram import InstagramSpider
from instagram_parser.ista_pars import settings

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    search = input('Write user ",": ')
    # search = 'vai_gogi'
    # search = 'toockay'
    search_l = [i.strip() for i in search.split(',')]
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstagramSpider, search=search_l)

    process.start()