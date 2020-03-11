# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MaoyanPipeline(object):
    def process_item(self, item, spider):
        print(item['name'], item['time'], item['star'])
        return item


# 存mtsql数据库
import pymysql
from .settings import *


class MaoyanMysqlPipeline(object):
    # 之执行一次用于数据库的连接
    def open_spider(self, spider):
        self.db = pymysql.connect(HOST, USER, PASSWORD, DATABASE, CHARSET)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        ins = 'insert into filmtab values(%s,%s,%s);'
        li = [item['name'], item['star'], item['time']]
        self.cursor.execute(ins, li)
        self.db.commit()
        return item

    # 之执行一次，用于数据库的断开
    def close_sipder(self, spider):
        self.cursor.close()
        self.db.close()

# 村入mongodb
import pymongo
class MaoyanMongoPipeline(object):
    def open_spider(self, spider):
        self.coon = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.mongodb = self.coon[MONGO_DATABASE]
        self.myset = self.mongodb[MONGO_SET]

    def process_item(self, item, spider):
        item_dict = dict(item)
        self.myset.insert_one(item_dict)
        return item

