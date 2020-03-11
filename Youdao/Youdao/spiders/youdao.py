# -*- coding: utf-8 -*-
import scrapy
import time
import random
from hashlib import md5
import json
from ..items import YoudaoItem
class YoudaoSpider(scrapy.Spider):
    name = 'youdao'
    allowed_domains = ['fanyi.youdao.com']
    # start_urls = ['http://fanyi.youdao.com/']
    word = input('请输入要翻译的单词>>')
    def start_requests(self):
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        salt,sign,ts=self.get_page(self.word)
        formdata = {
            'i': self.word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'ts': ts,
            'bv': 'cf156b581152bd0b259b90070b1120e6',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME'
        }
        # cookies = self.get_cookies()
        yield scrapy.FormRequest(url=url,formdata=formdata,callback=self.parse)
    #
    # def get_cookies(self):
    #     cookies_str ="OUTFOX_SEARCH_USER_ID=873539247@111.227.185.220; OUTFOX_SEARCH_USER_ID_NCOO=2052418467.4554772; JSESSIONID=aaas0VPCQ9zbzd4jBKlbx; ___rl__test__cookies=1581815825687"
    #     cookies={}
    #     for one in cookies_str.split('; '):
    #         key = one.split('=')[0]
    #         value = one.split('=')[1]
    #         cookies[key] = value
    #     return cookies
    def get_page(self,word):
        ts = str(int(time.time()*1000))
        salt=ts+str(random.randint(0,9))
        string = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()
        return salt,sign,ts

    def parse(self, response):
        item = YoudaoItem()
        html = json.loads(response.text)
        item['result'] = html['translateResult'][0][0]['tgt']
        yield item