# -*- coding: utf-8 -*-

import scrapy
from amsemailbot.items import AmsemailbotItem


class AmsEmailbotSpider(scrapy.Spider):
    name = "ams_email"
    # it seems that scrapy cannot read relative path of local files, one workaround is to host the html files on a simple web server
    start_urls = [
        'http://localhost:8000/saved_search_results/All_cmip5_Search_p0.html',
        'http://localhost:8000/saved_search_results/All_cmip5_Search_p1.html',
        'http://localhost:8000/saved_search_results/All_cmip5_Search_p2.html',
        'http://localhost:8000/saved_search_results/All_cmip5_Search_p3.html',
        'http://localhost:8000/saved_search_results/All_cmip6_Search_p0.html'
    ]

    def parse(self, response):
        for paper in response.css('a').css('.hlFld-Title'):
            title = paper.css('::text').get().strip()
            paper_link_partial = paper.css('a::attr(href)').get()
            if paper_link_partial is not None:
                paper_link = 'https://journals.ametsoc.org'+paper_link_partial
                yield response.follow(paper_link, callback=self.parse_paper, cb_kwargs=dict(paper_title=title),
                                      # cookies copied from browser
                                      cookies={
                                          'timezone': '480',
                                          'I2KBRCK': '1',
                                          'SERVER': 'WZ6myaEXBLEgydZ2mAfv9Q==',
                                          'MAID': 'VgkVcgEt2RlmTsDkochSCw==',
                                          'MACHINE_LAST_SEEN': '2020-03-18T07%3A57%3A31.313-07%3A00',
                                          'JSESSIONID': 'aaafZEL6gTxN0gJJyhOdx',
                                          'PLUID':'4emwzPUCjJbkAcUfxaaSq8UdNy4='
                                        }
                                    )

    def parse_paper(self, response, paper_title):
        item = AmsemailbotItem()
        item['title'] = paper_title
        item['author'] = response.css('span').css(
            '.hlFld-ContribAuthor::text').get()
        item['email'] = response.css('a').css('.email::text').get()
        yield item
