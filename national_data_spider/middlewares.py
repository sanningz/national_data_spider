# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import json
import logging
import requests
import random
from scrapy import signals
from fake_useragent import UserAgent
from requests.exceptions import ConnectionError
from .items import NodesItem, DataNameItem, DataItem


class ProxyMiddleware():
    def __init__(self, proxy_pool_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_pool_url = proxy_pool_url

    # 获取随机代理
    def _get_random_proxy(self):
        try:
            response = requests.get(self.proxy_pool_url)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_pool_url=crawler.settings.get('PROXY_POOL_URL')
        )

    # 使用代理发送请求
    def process_request(self, request, spider):
        proxy = self._get_random_proxy()
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            request.proxies = proxies
            self.logger.debug('Using Proxy' + json.dumps(proxy))
        else:
            self.logger.debug('No Valid Proxy')


class RandomUserAgentMiddleware(object):

    def __init__(self):
        self.agent = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.agent.random)
