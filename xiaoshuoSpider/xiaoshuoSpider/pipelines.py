# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os


class spiderPipeline:
    def __init__(self):
        self.result = "result/"

    def process_item(self, item, spider):
        # 获取传递过来的数据
        book_name = item["book_name"]
        chapter_name = item["chapter_name"]
        content = item["content"]
        # 判断文件夹是否已经创建
        if not os.path.exists(self.result + book_name):
            os.makedirs(self.result + book_name)
        # 判断章节是否已经爬取，未爬取，则写入
        if not os.path.exists(self.result + book_name + "/" + chapter_name):
            with open(self.result + book_name + "/" + chapter_name, "w", encoding="utf-8") as f:
                f.write(content)
        return item
