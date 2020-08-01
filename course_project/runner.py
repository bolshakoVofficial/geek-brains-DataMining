from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from vkparse import settings
from vkparse.spiders.vk import VkSpider

if __name__ == '__main__':
    scrapy_settings = Settings()
    scrapy_settings.setmodule(settings)
    process = CrawlerProcess(settings=scrapy_settings)
    process.crawl(VkSpider)
    process.start()
