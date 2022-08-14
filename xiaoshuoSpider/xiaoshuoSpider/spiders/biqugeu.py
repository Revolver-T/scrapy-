import scrapy

from xiaoshuoSpider.items import XiaoshuospiderItem


class BiqugeuSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['https://www.biqugeu.net/']
    start_urls = ["https://www.biqugeu.net/class/1_1.html"]

    def parse(self, response):
        # 解析a标签，得到小说名和详情章节目录页面地址
        booklist = response.xpath('//ul/li/span[@class="s2"]/a')
        # 循环爬取到的小说，将其章节目录页的链接存放入scrapy的爬取队列
        for i in booklist:
            # 章节目录页的url链接，
            href = "https://www.biqugeu.net" + i.xpath("./@href").extract_first()
            # 小说名称
            book_name = i.xpath("string(.)").extract_first()
            request = scrapy.Request(href, callback=self.parse_detail, dont_filter=True)
            # 将书名传递给下一个解析函数
            request.meta["book_name"] = book_name
            yield request

    def parse_detail(self, response):
        # 解析章节目录列表
        chapterList = response.xpath('//div[@class="listmain"]/dl/dd/a')
        # 循环获取章节目录信息
        for i in chapterList:
            href = "https://www.biqugeu.net" + i.xpath("./@href").extract_first()
            chapter_name = i.xpath("string(.)").extract_first()
            # 向下解析详情页
            request = scrapy.Request(href, callback=self.parse_content, dont_filter=True)
            request.meta["book_name"] = response.meta["book_name"]
            request.meta["chapter_name"] = chapter_name
            yield request

    def parse_content(self, response):
        # 此处需要使用extract().是因为本身xpath解析出来是一个列表，我们需要把列表中的所有数据取出来
        content = response.xpath('//div[@id="content"]').xpath("string(.)").extract()
        # 将list以换行符分割，转换成字符串
        content = "\n".join(content)
        # 将结果存入item，传到pipline里进行存储
        item = XiaoshuospiderItem()
        item["content"] = content.strip()
        item["book_name"] = response.meta["book_name"]
        item["chapter_name"] = response.meta['chapter_name']
        yield item
