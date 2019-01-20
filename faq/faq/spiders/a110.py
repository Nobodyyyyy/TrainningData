# -*- coding: utf-8 -*-
import scrapy


class A110Spider(scrapy.Spider):
    name = '110'
    #allowed_domains = ['www.110.com/ask/browse-c29.html']
    start_urls = ['http://www.110.com/ask/browse-c29.html/']

    def parsePages(self, response):
        question = response.xpath("//div[@class='leftbox01']/div[@class='wenz']/h1/text()").extract_first()
        answer = response.css("div.zjdanr::text").extract_first()
        questionDetailed = response.css("div.xwz::text").extract_first()

        yield {
            'question' : question,
            'questionDetailed' : questionDetailed,
            'answer' : answer
        }

    def parse(self, response):
        urls = response.xpath("//div[@class='leftbox02']/div[@class='tit07']/span[@class='g06']/a[@target]//@href").extract()
        for url in urls:
            yield scrapy.Request(url = 'http://www.110.com' + url, callback = self.parsePages)
        #翻页
        currentPage = response.xpath("//div[@class='pages']/table[@class='page-page']/tr/td[@class='page-current']/text()").extract_first()
        if int(currentPage) <= 100:
            nextPage = response.xpath("//div[@class='pages']/table[@class='page-page']/tr/td[last()-2]//@href").extract_first()
            yield scrapy.Request(url = 'http://www.110.com' + nextPage, callback = self.parse)