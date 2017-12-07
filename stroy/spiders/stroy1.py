# -*- coding: utf-8 -*-
import scrapy
from stroy.items import StroyItem

class Stroy1Spider(scrapy.Spider):
    name = 'stroy1'
    allowed_domains = ['xigushi.com']
    #start_urls = ['http://www.xigushi.com/zlgs/']
    #http://www.xigushi.com/zlgs/list_7_4.html
    baseUrl = "http://www.xigushi.com/zlgs/list_7_"
    offset = 1
    end =".html"
    start_urls = [baseUrl + str(offset) + end]

    def parse(self, response):
        node_list = response.xpath("//div[@class='list']/dl/dd/ul/li")
        
        for node in node_list:
            item = StroyItem()
            item["title"] = node.xpath("./a/text() | ./a/b/text()").extract()[0].encode("utf-8")
            item["link"] = node.xpath("./a/@href").extract()[0].encode("utf-8")
            cturl = "http://www.xigushi.com" + item["link"]

            yield scrapy.Request(
                url=cturl,
                callback=self.parseC,
                meta={"title": item['title'],"link": item['link'] }
            )
            #yield item



        if self.offset < 34:
            self.offset += 1
            url =self.baseUrl +str(self.offset) + self.end
            yield scrapy.Request(url,callback = self.parse)

    def parseC(self,response):
        content = response.xpath("//div[@class='by']/dl/dd//p").extract()[0].encode("utf-8")
        #content = response.xpath("//div[@class='novel']/div[@class='yd_text2']").extract()
        item = StroyItem()
        item['title'] = response.meta['title']
        item['link'] = response.meta['link']
        
        item['content'] = content
       # print item['title'], item['link']
        yield item
        #scrapy crawl stroy1