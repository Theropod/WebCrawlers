# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


def dbHandle():
    conn = MySQLdb.connect(
        host='localhost',
        user='Theropod',
        passwd='qpwoeiruty',
        use_unicode=True,
        #charset这一句不能省略，否则写不进数据库。注意mysql里utf8也有很多版本，而且没有中间的横线
        charset='utf8',
        port=3306,
    )
    return conn

class MyPipeline(object):
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        #Why the tuple? Because the DB API requires you to pass in any parameters as a sequence.
        #https://mysqlclient.readthedocs.io/en/latest/user_guide.html#some-examples
        # sql = 'insert into theropod.quotes (text,author,tags) values (%s,%s,%s)'
        # # values= (item['text'], item['author'], item['tags'])
        sql = 'insert into theropod.ow (Name,SkillRating,MatchesPlayed,Wins,Losses,WinningRate,KD,TimePlayed,TimeOnFire,' \
              'Hero1,H1ElmPerMnt,H1KD,H1Accur,H1HealPM,H1DmgPM,H1ObjKill,H1ObjTime,' \
              'Hero2,H2ElmPerMnt,H2KD,H2Accur,H2HealPM,H2DmgPM,H2ObjKill,H2ObjTime,' \
              'Hero3,H3ElmPerMnt,H3KD,H3Accur,H3HealPM,H3DmgPM,H3ObjKill,H3ObjTime)' \
              ' values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        values= (item['Name'],item['SkillRating'],item['MatchesPlayed'],item['Wins'],item['Losses'],item['WinningRate'],item['KD'],item['TimePlayed'],item['TimeOnFire'],
                 item['Hero1'],item['H1ElmPerMnt'],item['H1KD'],item['H1Accur'],item['H1HealPM'],item['H1DmgPM'],item['H1ObjKill'],item['H1ObjTime'],
                 item['Hero2'], item['H2ElmPerMnt'], item['H2KD'], item['H2Accur'], item['H2HealPM'], item['H2DmgPM'],item['H2ObjKill'], item['H2ObjTime'],
                 item['Hero3'], item['H3ElmPerMnt'], item['H3KD'], item['H3Accur'], item['H3HealPM'], item['H3DmgPM'],item['H3ObjKill'], item['H3ObjTime']
                 )
        # 只存2个测试一下
        # sql = 'insert into theropod.ow (Hero1,H1ElmPerMnt) values (%s,%s)'
        # values= (item['Hero1'],item['H1ElmPerMnt'])
        try:
            cursor.execute(sql,values)
            dbObject.commit()
        except Exception as e:
            print(e.args)
            dbObject.rollback()

        return item
