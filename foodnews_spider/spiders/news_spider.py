# -*- coding:utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from foodnews_spider.items import FoodnewsSpiderItem


class NewsSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ['cctv.com', 'cntv.cn']
    # start_urls = ['http://news.cntv.cn/20110601/102300.shtml']
    # TODO start_url测试使用新闻门户搜索结果页面，使用多层爬取
    start_urls = ['https://search.cctv.com/search.php?'
                  'qtext=%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E4%BA%8B%E4%BB%B6&sort'
                  '=relevance&type=web&vtime=&datepid=1&channel=&page=1']

    def parse(self, response):
        """
        搜索页面析取，第一层
        :param response:
        :return:
        """
        ld = ItemLoader(item=FoodnewsSpiderItem(), response=response)
        # ld.add_value('url', response.url)
        # ld.add_xpath('title', '//h1[@class="b-tit"]/text()')
        # ld.add_xpath('title', '//div[@class="cnt-bd"]/h1/text()')
        # ld.add_xpath('content', '//div[@class="cnt-bd"]/p/text()')
        # ld.add_xpath('content', '//div[@class="body"]/p/text()')
        return ld.load_item()

    def pagelist_parse(self, response):
        """
        从上一层获取搜索结果的一个列表页面
        :param response:
        :return:
        """
        pass

    def pagecontent_parse(self, response):
        """
        页面内容析取，第三层
        :param response:
        :return:
        """
        pass
