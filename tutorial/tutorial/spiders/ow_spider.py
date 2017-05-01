# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import MyItem
from scrapy.http.request import Request


class QuotesSpider(scrapy.Spider):
    # item = MyItem()
    name = "ow"
    start_urls = [
        'file:///E:/CAU/大三下/统计分析与建模/scrapy4ow/OwKorea_Score_files/OwKorea_Score.html',
    ]
    def parse(self, response):
        flag=0
        for player in response.css('div.table-row'):
            item = MyItem()
            # 第一个tablerow不能用
            if(flag==0):
                pass
            # 只走三次的测试
            # elif(flag==4):
            #     break
            else:
                # yield一次貌似就要执行一次pipeline，这里没获取完，不yield,而是把参数通过meta传到下一个parse里面
                # yield {
                # 'Name': player.css('span.table-name-block').css('strong::text').extract_first().strip(),
                # # 'Name': player.xpath('.//table-row-content/table-name/table-name-block').css('strong::text').extract_first(),
                # 'SkillRating': int(player.css('span.table-name-block').css('small').css('strong::text').extract_first().replace(',','')),
                # 'Wins': int(player.css('div.bar-container').css('span::text').extract_first().replace('W','')),
                # 'Losses': int(player.css('span.bar-losses::text').extract_first().replace('L','')),
                # 'MatchesPlayed': int(player.css('div.bar-container').css('span::text').extract_first().replace('W',''))+int(player.css('span.bar-losses::text').extract_first().replace('L','')),
                # 'WinningRate': float(player.css('div.bar-outer::text').extract_first().replace('%','')),
                # 'KD': float(player.css('div.kd-ratio-main').css('strong::text').extract_first()),
                # 'TimePlayed': int(player.css('div.time-played::text').extract_first().split(' ')[0]),
                # 'TimeOnFire':int(player.css('div.time-fire::text').extract_first().split(' ')[1])
                # }
                item['Name']=player.css('span.table-name-block').css('strong::text').extract_first().strip()
                # 有少数人没定级，不处理的话走到这个人这里就不往下走了
                item['SkillRating']= int(player.css('span.table-name-block').css('small').css('strong::text').extract_first().replace(',','')
                                         if player.css('span.table-name-block').css('small::text').extract_first()!='Unrated' else '0' )
                item['Wins']=int(player.css('div.bar-container').css('span::text').extract_first().replace('W',''))
                item['Losses']=int(player.css('span.bar-losses::text').extract_first().replace('L',''))
                item['MatchesPlayed']=int(player.css('div.bar-container').css('span::text').extract_first().replace('W',''))+int(player.css('span.bar-losses::text').extract_first().replace('L',''))
                item['WinningRate']=float(player.css('div.bar-outer::text').extract_first().replace('%',''))
                item['KD']=float(player.css('div.kd-ratio-main').css('strong::text').extract_first())
                item['TimePlayed']=int(player.css('div.time-played::text').extract_first().split(' ')[0])
                item['TimeOnFire']=int(player.css('div.time-fire::text').extract_first().split(' ')[1])
                next_page = player.css('a::attr(href)').extract_first()
                if next_page is not None:
                    # 没有cookie的话默认打开的是quick game的数据。
                    yield  Request(next_page,meta={'item': item},cookies={
                        '__cfduid':'d5ce69d519ce4017c6a21788674cab39d1492088444',
                        ' app-session':'p304m6kenv6emrpo05oamq00i7',
                        ' cdmu':'1492226219161',
                        ' bknx_fa':'1492226224962',
                        ' bknx_ss':'1492226224962',
                        ' cdmblk2':'0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0.16:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0',
                        ' _ga':'GA1.2.1115631317.1492088448',
                        ' __asc':'e1ee266f15b6fc321e850d3c078',
                        ' __auc':'bcb925c915b6766eb49bad29d47',
                        ' cdmabp':'true',
                        ' cdmblk':'0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0,0:0:0:0:0:0:0:0:0:0:0:0:0',
                        ' cdmtlk':'0:0:0:0:0:0:0:504:0:0:0:0:0',
                        ' cdmgeo':'cn',
                        ' cdmbaserate':'2.1',
                        ' cdmbaseraterow':'1.1',
                        ' cdmint':'0'
                        },callback=self.parse_detail)
            flag=1


    def parse_detail(self,response):
        heronumber=0
        item = response.meta['item']
        for heroes in response.css('div.heroes-details-card'):
            if(heronumber==0):
                    # 没有的数据会是一条'-'，换成0
                    item['Hero1']=heroes.css('div.card-hero-name').css('strong::text').extract_first()
                    item['H1MatchPlayed']=int(heroes.css('span.card-games::text').extract_first().split(' ')[0]
                                         if heroes.css('span.card-games::text').extract_first() is not None else '0')
                    item['H1ElmPerMnt']=float(heroes.css('div.stats-bar-percentile')[0].css('div.bar-value::text').extract_first()
                                         if heroes.css('div.stats-bar-percentile')[0].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H1KD']=float(heroes.css('div.stats-bar-percentile')[1].css('div.bar-value::text').extract_first()
                                 if heroes.css('div.stats-bar-percentile')[1].css('div.bar-value::text').extract_first() is not None else '0' )
                    item['H1Accur']=float(heroes.css('div.stats-bar-percentile')[2].css('div.bar-value::text').extract_first().split(' ')[0]
                                    if heroes.css('div.stats-bar-percentile')[2].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H1HealPM']=float(heroes.css('div.stats-bar-percentile')[4].css('div.bar-value::text').extract_first().replace(',','')
                                     if heroes.css('div.stats-bar-percentile')[4].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H1DmgPM']=float(heroes.css('div.stats-bar-percentile')[6].css('div.bar-value::text').extract_first().replace(',','')
                                    if heroes.css('div.stats-bar-percentile')[6].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H1ObjKill']=float(heroes.css('div.stats-bar-percentile')[7].css('div.bar-value::text').extract_first().split(' ')[0]
                                      if heroes.css('div.stats-bar-percentile')[7].css('div.bar-value::text').extract_first() is not None else '0')
                    # 这个有seconds的单位，去掉。
                    item['H1ObjTime']=float(heroes.css('div.stats-bar-percentile')[8].css('div.bar-value::text').extract_first().split(' ')[0]
                                      if heroes.css('div.stats-bar-percentile')[8].css('div.bar-value::text').extract_first() is not None else '0')
            elif(heronumber==1):
                    item['Hero2']=heroes.css('div.card-hero-name').css('strong::text').extract_first()
                    item['H2MatchPlayed']=int(heroes.css('span.card-games::text').extract_first().split(' ')[0]
                                         if heroes.css('span.card-games::text').extract_first() is not None else '0')
                    item['H2ElmPerMnt']=float(heroes.css('div.stats-bar-percentile')[0].css('div.bar-value::text').extract_first()
                                         if heroes.css('div.stats-bar-percentile')[0].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H2KD']=float(heroes.css('div.stats-bar-percentile')[1].css('div.bar-value::text').extract_first()
                                 if heroes.css('div.stats-bar-percentile')[1].css('div.bar-value::text').extract_first() is not None else '0' )
                    item['H2Accur']=float(heroes.css('div.stats-bar-percentile')[2].css('div.bar-value::text').extract_first()
                                    if heroes.css('div.stats-bar-percentile')[2].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H2HealPM']=float(heroes.css('div.stats-bar-percentile')[4].css('div.bar-value::text').extract_first().replace(',','')
                                     if heroes.css('div.stats-bar-percentile')[4].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H2DmgPM']=float(heroes.css('div.stats-bar-percentile')[6].css('div.bar-value::text').extract_first().replace(',','')
                                    if heroes.css('div.stats-bar-percentile')[6].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H2ObjKill']=float(heroes.css('div.stats-bar-percentile')[7].css('div.bar-value::text').extract_first()
                                      if heroes.css('div.stats-bar-percentile')[7].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H2ObjTime']=float(heroes.css('div.stats-bar-percentile')[8].css('div.bar-value::text').extract_first().split(' ')[0]
                                      if heroes.css('div.stats-bar-percentile')[8].css('div.bar-value::text').extract_first() is not None else '0')
            else:
                    item['Hero3']=heroes.css('div.card-hero-name').css('strong::text').extract_first()
                    item['H3MatchPlayed']=int(heroes.css('span.card-games::text').extract_first().split(' ')[0]
                                         if heroes.css('span.card-games::text').extract_first() is not None else '0')
                    item['H3ElmPerMnt']=float(heroes.css('div.stats-bar-percentile')[0].css('div.bar-value::text').extract_first()
                                         if heroes.css('div.stats-bar-percentile')[0].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H3KD']=float(heroes.css('div.stats-bar-percentile')[1].css('div.bar-value::text').extract_first()
                                 if heroes.css('div.stats-bar-percentile')[1].css('div.bar-value::text').extract_first() is not None else '0' )
                    item['H3Accur']=float(heroes.css('div.stats-bar-percentile')[2].css('div.bar-value::text').extract_first()
                                    if heroes.css('div.stats-bar-percentile')[2].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H3HealPM']=float(heroes.css('div.stats-bar-percentile')[4].css('div.bar-value::text').extract_first().replace(',','')
                                     if heroes.css('div.stats-bar-percentile')[4].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H3DmgPM']=float(heroes.css('div.stats-bar-percentile')[6].css('div.bar-value::text').extract_first().replace(',','')
                                    if heroes.css('div.stats-bar-percentile')[6].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H3ObjKill']=float(heroes.css('div.stats-bar-percentile')[7].css('div.bar-value::text').extract_first()
                                      if heroes.css('div.stats-bar-percentile')[7].css('div.bar-value::text').extract_first() is not None else '0')
                    item['H3ObjTime']=float(heroes.css('div.stats-bar-percentile')[8].css('div.bar-value::text').extract_first().split(' ')[0]
                                      if heroes.css('div.stats-bar-percentile')[8].css('div.bar-value::text').extract_first() is not None else '0')
            heronumber+=1
            if(heronumber==3):
                break
        yield item

