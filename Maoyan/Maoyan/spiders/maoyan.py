# -*- coding: utf-8 -*-
import scrapy
from ..items import MaoyanItem

class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4?offset=0']
    offset = 0
    def parse(self, response):
        dd_list = response.xpath('//dl[@class="board-wrapper"]/dd')
        item = MaoyanItem()
        for dd in dd_list:
            item['name'] = dd.xpath('./a/@title').extract_first()
            item['star'] = dd.xpath('.//p[@class="star"]/text()').extract()[0]
            item['time'] = dd.xpath('.//p[@class="releasetime"]/text()').get()
            # 交给管道文件
            yield item
        # 生成下一页的地址，入队列
        self.offset += 10
        if self.offset <=90:
            url = 'https://maoyan.com/board/4?offset='+str(self.offset)
            # 传给调度器
            yield scrapy.Request(url=url,callback=self.parse)