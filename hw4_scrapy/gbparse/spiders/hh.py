# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from hw4_scrapy.gbparse.items import HHItem


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?st=searchVacancy&L_profession_id=29.8&area=1&no_magic=true&text=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82+Python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[@data-qa="pager-block"]//a[@data-qa="pager-next"]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        for ad in response.xpath(
                '//a[@data-qa="vacancy-serp__vacancy-title"]/@href').extract():
            yield response.follow(ad, callback=self.post_parse)

    def post_parse(self, response: HtmlResponse):
        item = ItemLoader(HHItem(), response)
        item.add_xpath('title', '//h1/text()')
        item.add_value('url', response.url)
        item.add_xpath('salary', '//div[@class="vacancy-title"]//p')
        item.add_xpath('skills',
                       '//div[@class="vacancy-section"]//span[@class="bloko-tag__section bloko-tag__section_text"]/text()')
        item.add_xpath('hiring_org', '//a[@itemprop="hiringOrganization"]/span[@itemprop="name"]')
        item.add_xpath('org_url', '//a[@itemprop="hiringOrganization"]/@href')
        item.add_xpath('org_logo', '//div[@class="vacancy-company-wrapper"]//a[@class="vacancy-company-logo"]/@href')

        yield item.load_item()
