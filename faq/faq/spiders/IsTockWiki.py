# -*- coding: utf-8 -*-
import scrapy


class IstockwikiSpider(scrapy.Spider):
    name = 'IsTockWiki'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    start_urls = ['http://istock.stocom.net/wiki/doku.php?id=faq:start']

    def parse_faq(self, response):

        answer = response.css('div.level1 div.wrap_center p::text').extract()
        i = 0
        while i < len(answer):
            if answer[i].strip() == '':
                del answer[i]
            i += 1

        yield {
            'question' : answer[0],
            'answer' : answer[1]
        }

    def parse(self, response):
        for url in response.css('div.level3 p a::attr(href)').extract():
            print(url)
            yield scrapy.Request(url = 'http://istock.stocom.net'+ url, callback = self.parse_faq)
