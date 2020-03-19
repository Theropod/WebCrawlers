# -*- coding: utf-8 -*-

import os
import scrapy
from cnkioversea_crawler.items import CnkioverseaCrawlerItem


class CnkioverseaCrawlerSpider(scrapy.Spider):
    name = "cnki_oversea"

    def start_requests(self):
        urlfile="./cnki_paper_urls.csv"
        if os.path.exists(urlfile):
            for l in open(urlfile).readlines():
                start_url=l.strip().split(',')[1]
                id=l.strip().split(',')[0]
                yield scrapy.Request(url=start_url, callback=self.parse,cb_kwargs=dict(paperid=id))
        else:
            test_start_url='http://new.oversea.cnki.net/kcms/detail/61.1501.R.20200214.1311.004.html'
            test_id='447'
            yield scrapy.Request(url=test_start_url, callback=self.parse,cb_kwargs=dict(paperid=test_id))

    def parse(self, response, paperid):
        item = CnkioverseaCrawlerItem()
        ## except url, all fields could be empty, check before using list index
        # title
        title=response.css('.title::text').getall()
        if(title):
            item['title']=title[0]
        else:
            item['title']='N/A'

        # title_en
        title_en=response.css('.title::text').getall()
        if(len(title_en)>1):
            item['title_en']=title_en[1]
        else:
            item['title_en']='N/A'

        # remove spaces in keywords_en, and deal with empty cases
        keywords_en_raw=response.xpath('//div[@class="wxBaseinfo"]/p[5]/a/text()').getall()
        keywords_en=[]
        if(keywords_en_raw):
            for keywords in keywords_en_raw:
                keywords_en.append(keywords.strip())
            item['keywords_en']=' '.join(keywords_en)
        else:
            item['keywords_en']='N/A'

        # authors
        authors=response.css('.author').css('a::text').getall()
        if(authors):
            item['authors']=';'.join(authors)
        else:
            item['authors']='N/A'
    
        # journal name
        journal=response.css('.title').css('a::text').get()
        if(journal):
            item['journal']=journal
        else:
            item['journal']='N/A'

        # journal name en
        journal_en=response.xpath('//div[@class="sourinfo"]/p[2]/a/text()').get()
        if(journal_en):
            item['journal_en']=journal_en
        else:
            item['journal_en']='N/A'
        
        # id is not empty
        item['id']=paperid

        # responseurl is not empty
        item['response_url']=response.url

        # abstract en
        abstract_en=response.css('#ChDivSummaryen::text').get()
        if(abstract_en):
            item['abstract_en']=abstract_en
        else:
             item['abstract_en']='N/A'

        yield item