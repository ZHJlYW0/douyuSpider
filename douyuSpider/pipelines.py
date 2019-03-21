# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class DouyuspiderPipeline(object):
#     def process_item(self, item, spider):
#         return item
from os import rename
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

from douyuSpider.settings import IMAGES_STORE as images_store


class DouyuspiderPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['vertical_src'])

    def item_completed(self, results, item, info):
        # print('*' * 100)
        # print(results)
        # # [(True, {'url': 'https://rpic.douyucdn.cn/live-cover/appCovers/2019/03/13/5955015_20190313210852_big.jpg', 'checksum': 'b7f4b69a0544feeb9b5b3e0cdcd239aa', 'path': 'full/ae57da1722c66fe0c28d68db6b66ec9259d9b222.jpg'})]
        # # results == [(ok==True, x=={......})]
        # print('*' * 100)

        # 取出results里图片信息中的图片路径的值
        image_path = [x["path"] for ok, x in results if ok]

        # 移动文件并重命名文件名
        # rename(images_store + "/" + image_path[0],
        #        images_store + "/rename/" + item["nickname"] + " " + item["anchor_city"] + " " + image_path[0][5:-4] + ".jpg")
        rename(images_store + "/" + image_path[0],
               images_store + "/rename/" + item["nickname"] + " " + item["anchor_city"] + " " + image_path[0][5:])

        # 因为这里是该函数最后一行代码，使用return返回和使用yield返回效果一样
        return item
        # yield item
