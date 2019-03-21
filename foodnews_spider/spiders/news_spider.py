# -*- coding:utf-8 -*-

import scrapy
from scrapy.loader import ItemLoader
from foodnews_spider.items import FoodnewsSpiderItem
import json
from random import random


class NewsSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ['cctv.com', 'cntv.cn']
    # start_urls = ['http://news.cntv.cn/20110601/102300.shtml']
    # TODO start_url测试使用新闻门户搜索结果页面，使用多层爬取
    start_urls = [
        'https://search.cctv.com/search.php?qtext=%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E4%BA%8B%E4%BB%B6&type=web']

    def parse(self, response):
        """
        搜索页面析取，第一层
        :param response:
        :return:
        """
        # 获取当前搜索结果页面的页面链接信息，并传递给下一层解析器
        pageLinkList = response.xpath('//div[@class="tuwenjg"]//a[@id and @href]/@id').extract()
        pageLinkUrlList = response.xpath('//div[@class="tuwenjg"]//a[@id and @href]/@href').extract()
        # 页面链接的值需要提取处理
        pageLinkUrlList = [link[link.find('http'):link.find('html') + 4] for link in pageLinkUrlList]
        for i in range(len(pageLinkList)):
            if str(pageLinkList[i]).startswith('web_content'):
                yield scrapy.Request(pageLinkUrlList[i], meta={'url': pageLinkUrlList[i]},
                                     callback=self.cctv_page_parse)
        next_page = response.xpath('//a[@class="page-next"]').extract()
        if next_page:  # 如果搜索结果有下一页
            url = response.xpath('//a[@class="page-next"]//@href').extract()[0]
            url = "{}://{}/{}".format('http', response.url.split('/')[2], url)
            print('debug: nextpageurl = ', url)
            # 处理完毕当前页面的搜索结果，迭代处理下一个搜索页面
            yield scrapy.Request(url, callback=self.parse)

        return None
        # ld = ItemLoader(item=FoodnewsSpiderItem(), response=response)
        # ld.add_value('url', response.url)
        # ld.add_xpath('title', '//h1[@class="b-tit"]/text()')
        # ld.add_xpath('title', '//div[@class="cnt-bd"]/h1/text()')
        # ld.add_xpath('content', '//div[@class="cnt-bd"]/p/text()')
        # ld.add_xpath('content', '//div[@class="body"]/p/text()')
        # return ld.load_item()

    def cctv_page_parse(self, response):
        """
        页面内容解析,第二层
        :param response:
        :return:
        """
        print('debug: 第二层解析器获得url: ', response.url)
        ld = ItemLoader(item=FoodnewsSpiderItem(), response=response)
        ld.add_value('url', response.meta['url'])
        ld.add_xpath('title', '//h1[@class="b-tit"][1]/text()')
        ld.add_xpath('title', '//div[@class="cnt_bd"]/h1[1]/text()')
        ld.add_xpath('content', '//div[@class="cnt_bd"]/p/text()')
        ld.add_xpath('content', '//div[@class="body"]/p/text()')
        return ld.load_item()


class HuanqiuNewsSpider(scrapy.Spider):
    name = "huanqiu_spider"
    allowed_domains = ['huanqiu.com']
    start_urls = ['http://health.huanqiu.com/food_safety/']
    prev_url = ''  # 用于记录上一层解析的网页url

    def parse(self, response):
        """
        第一层析取
        :param response:
        :return:
        """
        pageLinks = response.xpath('//li[@class="item"]//a/@href').extract()
        pageLinks = list(set(pageLinks))
        for link in pageLinks:
            yield scrapy.Request(link, callback=self.page_parse)
        # 获取下一个第一层页面链接
        self.prev_url = response.url
        next_url = response.xpath('//a[@class="a1"][last()]/@href').extract()[0]
        if next_url and self.prev_url != next_url:
            yield scrapy.Request(next_url, callback=self.parse)
        return None

    def page_parse(self, response):
        """
        第二层析取，爬取新闻页面内容
        :param response:
        :return:
        """
        ld = ItemLoader(item=FoodnewsSpiderItem(), response=response)
        ld.add_value('url', response.url)
        ld.add_xpath('title', '//h1[@class="tle"][1]/text()')
        ld.add_xpath('title', '//div[@class="conText"]/h1[1]/text()')
        ld.add_xpath('content', '//div[@class="la_con"]//p/text()')
        ld.add_xpath('content', '//div[@class="conText"]//p/text()')
        return ld.load_item()


class SinaNewsSpider(scrapy.Spider):
    name = 'sina_spider'
    allowed_domains = ['sina.com.cn']
    MAX_GET=100000
    # start_urls = [
    #     'http://api.search.sina.com.cn/?c=news&q=%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8&page=1']
    start_urls=['http://api.search.sina.com.cn/?c=news&q=%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8&page='+str(i) for i in range(MAX_GET)]

    def parse(self, response):
        """
        sina食品安全搜索结果页面第一层爬取解析
        :param response:
        :return:
        """
        url = str(response.url)
        # 获得页面的json数据
        try:
            jsdata = json.loads(str(response.body.decode('utf-8')))
            pageUrls = [jsdata['result']['list'][j]['url'] for j in range(0, 20)]
            print('debug: currurl={}, pagelinks={}'.format(url, pageUrls))
            for pagelink in pageUrls:
                yield scrapy.Request(pagelink, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                     callback=self.parse_page, dont_filter=True)
        except:
            # 处理页面重定向导致的问题, 重新请求
            print('my debug: parse error occur!!')
            yield scrapy.Request(url, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                 callback=self.parse, dont_filter=True)
        return None

    def parse_page(self, response):
        """
        解析新闻内容页面
        :param response:
        :return:
        """
        ld = ItemLoader(item=FoodnewsSpiderItem(), response=response)
        ld.add_value('url', response.url)
        ld.add_xpath('title', '//h1[@class="main-title"]//text()')
        ld.add_xpath('title', '//div[@class="article-header clearfix"]/h1//text()')
        ld.add_xpath('title', '//h2[@class="titName 5G_txta"]//text()')
        ld.add_xpath('content', '//div[@id="artibody"]//p/font//text()')
        ld.add_xpath('content', '//div[@id="artibody"]//p//text()')
        ld.add_xpath('content', '//div[@class="article-body main-body"]//p//text()')
        ld.add_xpath('content', '//div[@id="article"]//p//text()')
        ld.add_xpath('content', '//div[@id="sina_keyword_ad_area2"]//p//text()')
        return ld.load_item()
