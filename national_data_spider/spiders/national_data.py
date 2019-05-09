# -*- "coding": "utf-8 -*-",
import json
import time
import scrapy
from urllib.parse import urlencode
from ..items import NodesItem, DataNameItem, DataItem
from ..settings import DBCODE

CURRENT_TIME = str(int(time.time()))


class NationalDataSpider(scrapy.Spider):
    name = 'national_data'

    global CURRENT_TIME
    # 获取数据接口
    tree = {
        "id": "zb",
        "dbcode": DBCODE,
        "wdcode": "zb",
        "m": "getTree",
    }

    allowed_domains = ['data.stats.gov.cn']
    start_urls = ['http://data.stats.gov.cn/easyquery.htm?' + urlencode(tree),
                  ]

    def parse(self, response):
        # 获取下级结点信息
        tree = scrapy.Selector(response).xpath('//p/text()').extract_first()
        tree = json.loads(tree)
        for i in tree:
            # 储存下级结点信息
            item = NodesItem()
            item['dbcode'] = i['dbcode']
            item['name'] = i['name']
            item['id'] = i['id']
            item['wdcode'] = i['wdcode']
            item['pid'] = i['pid']
            yield item
            del i['name']
            del i['pid']
            # 检查是否存在下级结点
            if i['isParent']:
                # 格式化下级结点url
                i['m'] = 'getTree'
                del i['isParent']
                node_url = 'http://data.stats.gov.cn/easyquery.htm?' + urlencode(i)
                print(node_url)
                # 请求下级结点
                yield scrapy.Request(url=node_url, callback=self.parse)
            # 格式化数据url
            # todo 地区url分析
            else:
                i['m'] = 'QueryData'
                i['rowcode'] = 'zb'
                i['colcode'] = 'sj'
                i['wds'] = '[]'
                i['dfwds'] = '[{"wdcode":"wd","valuecode":"value"}]'.replace('"wd"', '"' + i['wdcode'] + '"')\
                                                                    .replace('"value"', '"' + i['id'] + '"')
                i['k1'] = CURRENT_TIME
                del i['id']
                del i['wdcode']
                data_url = 'http://data.stats.gov.cn/easyquery.htm?' + urlencode(i).replace('%27', '%22')
                # 请求数据
                yield scrapy.Request(url=data_url, callback=self.data_parse)
                '''
                # 请求最近36个月数据
                # 需在请求相关数据后发送请求
                i['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST36"}]'
                i['k1'] = CURRENT_TIME
                data_36_url = 'http://data.stats.gov.cn/easyquery.htm?' + urlencode(i).replace('%27', '%22')
                yield scrapy.Request(url=data_url, callback=self.data_parse)
                '''

    def data_parse(self, response):
        data = scrapy.Selector(response).xpath('//p/text()').extract_first()
        data = json.loads(data)['returndata']
        data_nodes = data['datanodes']
        tag_nodes = data['wdnodes'][0]['nodes']

        # 储存指标名
        for i in tag_nodes:
            item = DataNameItem()
            item['name'] = i['name']
            item['memo'] = i['memo']
            item['zb'] = i['code']
            yield item
        # 储存数据
        for j in data_nodes:
            item = DataItem()
            item['zb'] = j['wds'][0]['valuecode']
            item['sj'] = j['wds'][1]['valuecode']
            if j['data']['hasdata']:
                item['data_str'] = j['data']['strdata']
            else:
                item['data_str'] = 'null'
            yield item
