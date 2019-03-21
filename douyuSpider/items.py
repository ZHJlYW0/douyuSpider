# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 垂直图片链接
    vertical_src = scrapy.Field()
    # 昵称
    nickname = scrapy.Field()
    # 锚定城市
    anchor_city = scrapy.Field()
