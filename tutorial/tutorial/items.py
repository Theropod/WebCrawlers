# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 注意：前三多的英雄的数据的item名字可以一样，反正要入库的。
    Name = scrapy.Field()
    SkillRating = scrapy.Field()
    MatchesPlayed = scrapy.Field()
    Wins = scrapy.Field()
    Losses = scrapy.Field()
    WinningRate = scrapy.Field()
    KD = scrapy.Field()
    TimePlayed = scrapy.Field()
    TimeOnFire = scrapy.Field()
    # OnFirePctg = scrapy.Field()
    Hero1 = scrapy.Field()
    # H1TimePlayed = scrapy.Field()
    H1ElmPerMnt = scrapy.Field()
    H1KD = scrapy.Field()
    H1Accur = scrapy.Field()
    H1HealPM = scrapy.Field()
    H1DmgPM = scrapy.Field()
    H1ObjKill = scrapy.Field()
    H1ObjTime = scrapy.Field()
    Hero2 = scrapy.Field()
    # H2TimePlayed = scrapy.Field()
    H2ElmPerMnt = scrapy.Field()
    H2KD = scrapy.Field()
    H2Accur = scrapy.Field()
    H2HealPM = scrapy.Field()
    H2DmgPM = scrapy.Field()
    H2ObjKill = scrapy.Field()
    H2ObjTime = scrapy.Field()
    Hero3 = scrapy.Field()
    # H3TimePlayed = scrapy.Field()
    H3ElmPerMnt = scrapy.Field()
    H3KD = scrapy.Field()
    H3Accur = scrapy.Field()
    H3HealPM = scrapy.Field()
    H3DmgPM = scrapy.Field()
    H3ObjKill = scrapy.Field()
    H3ObjTime = scrapy.Field()

