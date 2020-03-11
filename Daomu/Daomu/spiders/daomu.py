# -*- coding: utf-8 -*-
import scrapy
from ..items import DaomuItem

class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    def parse(self, response):

        link_list = response.xpath('//li[contains(@id,"menu-item-20")]/a')
        for li in link_list:
            item = DaomuItem()
            item['title'] = li.xpath('./text()').get()
            href = li.xpath('./@href').get()
            # 把所有的href交给调度器
            yield scrapy.Request(url=href,meta={'item':item},callback=self.parse_two_page)
    # 二级页面解析
    def parse_two_page(self,request):
        # 接受item
        item = request.meta['item']
        art_list = request.xpath('//article')
        for art in art_list:
            name = art.xpath('./a/text()').get()
            link = art.xpath('./a/@href').get()
            # 把章节连接交给调度器
            yield scrapy.Request(url=link,meta={'item':item,'name':name},callback=self.parse_three_page)
    # 三级页面解析
    def parse_three_page(self,request):
        item = request.meta['item']
        item['name'] = request.meta['name']
        # 体小说内容
        content_list = request.xpath('//article[@class="article-content"]/p/text()').extract()
        item['content'] = '\n'.join(content_list)
        yield item