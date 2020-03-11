# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
class DaomuPipeline(object):
    def process_item(self, item, spider):
        # '/home/mrdai/daomu/xxx'
        director = '/home/mrdai/daomu/{}/'.format(item['title'])
        if not os.path.exists(director):
            os.makedirs(director)
        # 写入文件
        filename = director + item['name'].replace(' ','_')+'.txt'
        with open(filename,'w') as f:
            f.write(item['content'])
        return item
