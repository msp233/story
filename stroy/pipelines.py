# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from scrapy.crawler import Settings as Settings 
class StroyPipeline(object):
    def __init__(self):
        
        dbargs = dict(
            host = '127.0.0.1' ,
            db = 'newboy',
            user = 'root', #replace with you user name
            passwd = '123456', # replace with you password
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
            )    
        self.dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)



        


    


    def process_item(self, item,spider):
        res = self.dbpool.runInteraction(self.insert_into_table,item)
        return item

    def insert_into_table(self,conn,item):
             conn.execute('insert into nb_story(title,content) values(%s,%s)', (item['title'],item['content']))
