# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

# from scrapy.exporters import JsonItemExporter
# 以jl格式输出
# from scrapy.exporters import JsonLinesItemExporter
# 以csv格式输出
from scrapy.exporters import CsvItemExporter
from scrapy import signals

import os

class CnkioverseaCrawlerPipeline(object):
    def process_item(self, item, spider):
        # only need url to identify papers
        if item.get('response_url'):
            return item
        else:
            raise DropItem('Missing RESPONSE URL')  
        return item
