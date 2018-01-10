# -*- coding: utf-8 -*-
import scrapy


class DrugsMainSpider(scrapy.Spider):
    name = 'drugs_main'
    allowed_domains = ['drugs.com']
    start_urls = ['https://www.drugs.com/alpha/a1.html']

    def parse(self, response):
        results = response.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/ul/li/a/@href')

        for number, link in enumerate(results, 1):
            print("{}. {}" .format(number, link.extract()))


        #pass
