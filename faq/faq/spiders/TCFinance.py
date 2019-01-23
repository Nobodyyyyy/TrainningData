# -*- coding: utf-8 -*-
import scrapy


class TcfinanceSpider(scrapy.Spider):
    name = 'TCFinance'
    start_urls = ['https://finance.qq.com/stock/college/zhqzs/news.htm']

    def parsePage(self, response):
        title = response.xpath("//div[@id='C-Main-Article-QQ']/div/h1/text()").extract_first()
        article = response.xpath("//div[@id='Cnt-Main-Article-QQ']/p/text()").extract()
        #article以列表方式存储，每个元素表示一段
        yield {
            'title' : title,
            'article' : article
        }

    def parse(self, response):
        urls = response.xpath("//div[@id='listZone']/table/tr/td/a/@href").extract()

        for url in urls:
            yield scrapy.Request(url = "https://finance.qq.com" + url, callback=self.parsePage)