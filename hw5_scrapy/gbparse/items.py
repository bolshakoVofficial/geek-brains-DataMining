# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class FollowersItem(scrapy.Item):
    _id = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    follower_name = scrapy.Field()
    follower_id = scrapy.Field()
    data = scrapy.Field()


class FollowingItem(scrapy.Item):
    _id = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    following_name = scrapy.Field()
    following_id = scrapy.Field()
    data = scrapy.Field()
