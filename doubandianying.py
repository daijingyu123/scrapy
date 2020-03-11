import requests
from fake_useragent import UserAgent
import time
import random
import json
import re

class Douban:
    def __init__(self):
        self.url = 'https://movie.douban.com/j/chart/top_list?type={}&interval_id=100%3A90&action=&start={}&limit=20'
        self.count = 0

    # 发送请求
    def get_html(self,url):
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,headers=headers).text
        return html
    # 解析
    def parse_html(self,url):

        html = json.loads(self.get_html(url))
        item = {}
        for page in html:
            item['name'] = page['title']
            item['time'] = page['release_date']
            item['star'] = page['actors']
            print(item)
            self.count += 1

    # 获取电影宗页数
    def get_total(self,choice):
        url = 'https://movie.douban.com/j/chart/top_list_count?type={}&interval_id=100%3A90'.format(choice)
        html = json.loads(self.get_html(url))
        total = html['total']
        print(total)
        # if total%20 == 0:
        #     total = total//20
        # else:
        #     total = total//20 +1
        return total

    # 获取类别
    def get_all_type_dict(self):
        type_url = 'https://movie.douban.com/chart'
        type_html = self.get_html(type_url)
        p = re.compile('<a href=".*?type_name=(.*?)&type=(.*?)&interval_id=100:90&action=">',re.S)
        r_list = p.findall(type_html)
        all_type_dict = {}
        for r in r_list:
            all_type_dict[r[0]] = r[1]
        return all_type_dict

    def run(self):
        # 获取类别
        # {'剧情':11,'喜剧'：23,...}
        all_type_dict = self.get_all_type_dict()
        menu = ''
        for name in all_type_dict:
            menu = menu + name + '|'
        while True:
            print(menu)
            choice = input('请输入类别>>')
            if choice in menu:
                total = self.get_total(all_type_dict[choice])
                for start in range(0,total,20):
                    url = self.url.format(all_type_dict[choice],start)
                    self.parse_html(url)

                    time.sleep(random.uniform(1,2))
                print(self.count)
                break
            else:
                print('没有此类别电影，清重新输入')
                continue



if __name__ == '__main__':
    douban = Douban()
    douban.run()











