# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import json


class VkSpider(scrapy.Spider):
    name = 'vk'
    allowed_domains = ['vk.com']
    start_urls = ['https://vk.com/']

    vk_login_link = 'https://login.vk.com/?act=login'
    source_url = 'https://vk.com/id122483091'
    target_url = 'https://vk.com/id29204850'

    vk_login = '+79154179464'
    vk_pass = 'mnx4xkue1996pass'

    def parse(self, response):
        yield scrapy.FormRequest(
            self.vk_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'email': self.vk_login, 'pass': self.vk_pass},
        )

    def user_parse(self, response: HtmlResponse):
        print(1)
