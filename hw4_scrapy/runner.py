from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gbparse import settings
from gbparse.spiders.hh import HhSpider

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    process.crawl(HhSpider)
    process.start()
