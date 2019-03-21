# -*- coding: utf-8 -*-
from json import loads, dumps

import scrapy

from douyuSpider.items import DouyuspiderItem


class DouyuSpider(scrapy.Spider):
    name = "douyu"
    allowed_domains = ["douyucdn.cn"]
    # start_urls = ('http://www.douyucdn.cn/',)
    baseURL = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset={}"
    offset = 0
    start_urls = [baseURL.format(offset)]

    def __init__(self):
        self.f1 = open("斗鱼主播信息.json", mode="w", buffering=-1, encoding="utf-8", errors="ignore")
        self.f2 = open("斗鱼主播信息2.json", mode="w", buffering=-1, encoding="utf-8", errors="ignore")
        print("不管翻多少页，只打开文件一次")

    def parse(self, response):
        body_bytes = response.body

        body_bytes_decode_to_str = response.body.decode("utf-8")
        # with open("斗鱼主播信息.json", mode="a", buffering=-1, encoding="utf-8", errors="ignore") as f:
        #     f.write(body_bytes_decode_to_str)
        #     f.write(", \n")
        self.f1.write(body_bytes_decode_to_str)
        self.f1.write(", \n")

        body_str_loads_to_dict = loads(response.body.decode("utf-8"), encoding="utf-8")

        body_dict_dumps_to_str = dumps(body_str_loads_to_dict, ensure_ascii=False)
        # with open("斗鱼主播信息2.json", mode="a", buffering=-1, encoding="utf-8", errors="ignore") as f:
        #     f.write(body_dict_dumps_to_str)
        #     f.write(", \n")
        self.f2.write(body_dict_dumps_to_str)
        self.f2.write(", \n")

        data_value = loads(response.body.decode("utf-8"))["data"]

        data_list = data_value

        if not data_list:
            return

        # 返回item给管道
        for i in data_list:
            # print('*' * 100)
            # print(i["vertical_src"])
            # print(i["nickname"])
            # print(i["anchor_city"])
            # print('*' * 100)

            # 创建item对象
            item = DouyuspiderItem()

            """防止程序中断"""
            # 方式一：判断
            if len(str(i["vertical_src"])):
                item["vertical_src"] = i["vertical_src"]
            else:
                item["vertical_src"] = ""
            if len(str(i["nickname"])):
                item["nickname"] = i["nickname"]
            else:
                item["nickname"] = ""
            if len(str(i["anchor_city"])):
                item["anchor_city"] = i["anchor_city"]
            else:
                item["anchor_city"] = ""

            # # 方式二：捕获异常
            # try:
            #     item["vertical_src"] = i["vertical_src"]
            # except Exception as ex:
            #     print(ex)
            #     item["vertical_src"] = ""
            # try:
            #     item["nickname"] = i["nickname"]
            # except Exception as ex:
            #     print(ex)
            #     item["nickname"] = ""
            # try:
            #     item["anchor_city"] = i["anchor_city"]
            # except Exception as ex:
            #     print(ex)
            #     item["anchor_city"] = ""

            # 返回item给管道
            yield item

        # 返回Request给调度器
        self.offset += 20
        yield scrapy.Request(self.baseURL.format(self.offset), callback=self.parse)

    def __del__(self):
        self.f1.close()
        self.f2.close()
        print("不管翻多少页，只关闭文件一次")
