# -*- coding: utf-8 -*-
import requests
import scrapy
from urllib import parse
import json
from ..items import TencentItem
class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    # start_urls = ['http://careers.tencent.com/']
    one_url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1566266592644&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1566266695175&postId={}&language=zh-cn'
    headers = {'User-Agent': 'Mozilla/5.0'}
    keyword = input('请输入职位：')
    keyword = parse.quote(keyword)

    def start_requests(self):
        """生成以及页面地址，交给调度器"""
        total = self.get_total()
        for index in range(1,total):
            url = self.one_url.format(self.keyword,index)
            yield scrapy.Request(url=url,callback=self.parse_one_page)


    def get_total(self):
        """获取宗页数"""
        url = self.one_url.format(self.keyword,1)
        html = requests.get(url=url,headers=self.headers).json()
        count = html['Data']['Count']
        if count % 10 ==0:
            total = count//10+1
        else:
            total = count//10+2
        return total

    def parse_one_page(self, response):
        """解析一级页面，提取postid"""
        one_html = json.loads(response.text)
        for one in one_html['Data']['Posts']:
            # postId ,two_url
            postid = one['PostId']
            url = self.two_url.format(postid)

            yield scrapy.Request(
                url=url,
                callback=self.parse_two_page
            )

    def parse_two_page(self,request):
        """提取具体数据"""
        item = TencentItem()
        two_html = json.loads(request.text)
        # 名称+类别+职责+要求+地址+时间
        item['job_name'] = two_html['Data']['RecruitPostName']
        item['job_type'] = two_html['Data']['CategoryName']
        item['job_duty'] = two_html['Data']['Responsibility']
        item['job_require'] = two_html['Data']['Requirement']
        item['job_address'] = two_html['Data']['LocationName']
        item['job_time'] = two_html['Data']['LastUpdateTime']

        yield item