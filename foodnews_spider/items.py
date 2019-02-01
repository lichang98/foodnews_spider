# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Compose, MapCompose


def rmSpace(value):
    """删除空白字符以及其他unicode等无效字符"""
    return value.strip('').replace('\r', ''). \
        replace('\n', '').replace('\t', '').replace(u'\u3000', '').replace('\xa0', '').strip()

def rmEmpty(lst):
    """删除列表中的空项目"""
    return list(filter(lambda x: x != '',lst))

class FoodnewsSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(input_processor=MapCompose(rmSpace),
                         output_processor=TakeFirst())
    content = scrapy.Field(serializer=str,
                           input_processor=MapCompose(rmSpace),
                           output_processor=Compose(rmEmpty))
    # title = scrapy.Field(output_processor=
    #                      Compose(lambda titlst:
    #                              [item.replace('\r', '').replace('\t', '').
    #                              replace('\n', '').strip(' ') for item in titlst]))
    # content = scrapy.Field(serializer=str,
    #                        output_processor=
    #                        Compose(lambda lst: [item.replace(u'\u3000', '').replace('\r','').replace('\n','')
    #                                             .replace('\t','')
    #                                             .replace('\xa0','').strip() for item in lst]))
