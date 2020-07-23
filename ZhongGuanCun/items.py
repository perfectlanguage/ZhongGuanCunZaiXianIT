# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhongguancunItem(scrapy.Item):
    # define the fields for your item here like:
    产品分类 = scrapy.Field()
    对应分类链接 = scrapy.Field()
    对应二级分类链接 = scrapy.Field()
    对应品牌分类链接 = scrapy.Field()
    产品链接 = scrapy.Field()
    产品名称 = scrapy.Field()
    产品参考价 = scrapy.Field()
    产品评分 = scrapy.Field()
    产品评论量 = scrapy.Field()
    产品介绍 = scrapy.Field()
    下载时间 = scrapy.Field()

