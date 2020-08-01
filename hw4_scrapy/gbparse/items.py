# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def fix_links(link: str):
    return str('https://hh.ru' + link)


def fix_org_name(name: str):
    result = name.split('">')
    result = result[1][:-7]

    if result.find('<!-- -->') != -1:
        result = result.split('<!-- -->')

    new_name = ''
    for i in range(len(result)):
        new_name += result[i]
    return new_name


def fix_salary(salary: str):
    result = salary.split('">')
    result = result[1].split('<!-- -->')
    new_salary = ''
    for i in range(len(result)):
        new_salary += result[i]
    new_salary = new_salary[:-4]

    return new_salary


class HHItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(input_processor=MapCompose(fix_salary),
                          output_processor=TakeFirst())
    skills = scrapy.Field()
    hiring_org = scrapy.Field(input_processor=MapCompose(fix_org_name),
                              output_processor=TakeFirst())
    org_url = scrapy.Field(input_processor=MapCompose(fix_links),
                           output_processor=TakeFirst())
    org_logo = scrapy.Field(input_processor=MapCompose(fix_links),
                            output_processor=TakeFirst())
    pass
