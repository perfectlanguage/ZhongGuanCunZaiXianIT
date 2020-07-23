# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from ZhongGuanCun.settings import MONGO_URL, MONGO_DBNAME, MONGO_COLLECTION


class ZhongguancunPipeline:
    def open_spider(self, spider):
        self.cli = pymongo.MongoClient(MONGO_URL)
        self.dbs = self.cli[MONGO_DBNAME]
        self.coll = self.dbs[MONGO_COLLECTION]

    def process_item(self, item, spider):
        data = dict(item)
        self.coll.insert(data)
        return item

    def close_spider(self, spider):
        self.cli.close()
