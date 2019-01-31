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
                  'qtext=%E9%A3%9F%E5%93%81%E5%AE%89%E5%85%A8%E4%BA%8B%E4%BB%B6&type=web']

    def parse(self, response):
        """
        搜索页面析取，第一层
        :param response:
        :return:
        """
        # 获取当前搜索结果页面的页面链接信息，并传递给下一层解析器
        pageLinkList = response.xpath('//div[@class="tuwenjg"]//a[@id and @href]/@id').extract()
        pageLinkUrlList = response.xpath('//div[@class="tuwenjg"]//a[@id and @href]/@href').extract()
        print('debug: pagelinklist len = {}, : {}'.format(len(pageLinkList),pageLinkList))
        print('debug: pageurllist len = {}, :{}'.format(len(pageLinkUrlList),pageLinkUrlList))
        # 页面链接的值需要提取处理
        pageLinkUrlList = [link[link.find('http'):link.find('html')+4] for link in pageLinkUrlList]
        for i in range(len(pageLinkList)):
            if str(pageLinkList[i]).startswith('web_content'):
                print('debug: request page url is ',pageLinkUrlList[i])
                yield scrapy.Request(pageLinkUrlList[i], meta={'url': pageLinkUrlList[i]}, callback=self.page_parse)
        next_page = response.xpath('//a[@class="page-next"]').extract()
        if next_page:  # 如果搜索结果有下一页
            url = response.xpath('//a[@class="page-next"]//@href').extract()[0]
            url = "{}://{}/{}".format('http',response.url.split('/')[2],url)
            print('debug: nextpageurl = ',url)
            # 处理完毕当前页面的搜索结果，迭代处理下一个搜索页面
            yield scrapy.Request(url,callback=self.parse)

        return None
        # ld = ItemLoader(item=FoodnewsSpiderItem(), response=response)
        # ld.add_value('url', response.url)
        # ld.add_xpath('title', '//h1[@class="b-tit"]/text()')
        # ld.add_xpath('title', '//div[@class="cnt-bd"]/h1/text()')
        # ld.add_xpath('content', '//div[@class="cnt-bd"]/p/text()')
        # ld.add_xpath('content', '//div[@class="body"]/p/text()')
        # return ld.load_item()

    def page_parse(self, response):
        """
        页面内容解析,第二层
        :param response:
        :return:
        """
        print('debug: 第二次解析器获得url: ',response.meta['url'])
        return None

