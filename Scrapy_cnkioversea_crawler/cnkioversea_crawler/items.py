# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnkioverseaCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=scrapy.Field()
    title=scrapy.Field()
    title_en=scrapy.Field()
    authors=scrapy.Field()
    journal=scrapy.Field()
    journal_en=scrapy.Field()
    response_url=scrapy.Field()
    keywords_en=scrapy.Field()
    abstract_en=scrapy.Field()
    pass
