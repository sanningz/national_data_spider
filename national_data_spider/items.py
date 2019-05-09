# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 节点数据
class NodesItem(scrapy.Item):
    dbcode = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    wdcode = scrapy.Field()
    pid = scrapy.Field()

    # sql操作
    def save_mysql(self, cursor, item):
        # 忽略已存在的数据
        sql = "INSERT IGNORE INTO Nodes(dbcode, name, id, wdcode, pid) VALUES ('{}','{}','{}','{}','{}')".format(self['dbcode'], self['name'], self['id'], self['wdcode'], self['pid'])
        cursor.execute(sql)


# 数据名称
class DataNameItem(scrapy.Item):
    name = scrapy.Field()
    memo = scrapy.Field()
    zb = scrapy.Field()

    def save_mysql(self, cursor, item):
        sql = "INSERT IGNORE INTO DataName(name, memo, zb) VALUES ('{}','{}','{}')".format(self['name'], self['memo'], self['zb'])
        cursor.execute(sql)


# 数据详情
class DataItem(scrapy.Item):
    sj = scrapy.Field()
    data_str = scrapy.Field()
    zb = scrapy.Field()

    def save_mysql(self, cursor, item):
        sql = "INSERT INTO Data(sj, data_str, zb) VALUES ('{}','{}','{}')".format(self['sj'], self['data_str'], self['zb'])
        cursor.execute(sql)

