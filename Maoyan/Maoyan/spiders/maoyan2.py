# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan2'
    allowed_domains = ['maoyan.com']
    # start_urls = ['https://maoyan.com/board/4?offset=0']
    url = 'https://maoyan.com/board/4?offset={}'
    # 重写start_request
    def start_requests(self):
        for offert in range(0,100,10):
            url = self.url.format(offert)
            # 交给调度器
            yield scrapy.Request(url=url,callback=self.parse_html)
    def parse_html(self, response):
        dd_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        item = MaoyanItem()
        for dd in dd_list:
            item['name'] = dd.xpath('./a/@title').extract_first()
            item['star'] = dd.xpath('.//p[@class="star"]/text()').extract()[0]
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').get()
            # 交给管道文件
            yield item
