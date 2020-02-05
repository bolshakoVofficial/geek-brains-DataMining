# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/kvartiry/prodam?cd=1']

    def parse(self, response: HtmlResponse):
        next_pages = response.css('.pagination-page::attr(href)').extract()
        for url in next_pages:
            yield response.follow(url, callback=self.parse)

            ads = response.css('.item__line a[class=snippet-link]::attr(href)').extract()

            for ad in ads:
                yield response.follow(ad, callback=self.post_parse)

        pass

    def post_parse(self, response: HtmlResponse):
        title = response.css('.title-info-title-text::text').extract()[0]
        price = response.css('.js-item-price::text').extract()[0]
        params_name = response.css('.item-params-list-item .item-params-label::text').extract()
        params_value = response.css('.item-params-list-item::text').extract()

        try:
            for _ in range(len(params_value) // 2):
                params_value.remove(' ')
        except:
            pass

        params = dict(zip(params_name, params_value))

        yield {
            'title': title,
            'price': price,
            'params': params,
        }

        pass
