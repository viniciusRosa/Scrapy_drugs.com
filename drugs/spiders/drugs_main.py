# -*- coding: utf-8 -*-
import scrapy


class DrugsMainSpider(scrapy.Spider):
    name = 'drugs_main'
    allowed_domains = ['drugs.com']
    first_page_url = ('https://www.drugs.com/alpha/a{}.html')

    def __init__(self):
        self.last_page = None


    def start_requests(self):
        request = scrapy.Request(
            url=DrugsMainSpider.first_page_url.format(1),
            callback=self.parse_page,
        )
        yield request

    def parse_page(self, response):
        self.last_page = int(response.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[2]/table/tr/td[2]/a/text()')[-1].extract())

        for page in range(1, self.last_page + 1):
            print(page)
            request = scrapy.Request(
                url=DrugsMainSpider.first_page_url.format(page),
                callback=self.parse_drugs_link,
            )
            print(DrugsMainSpider.first_page_url.format(page))
            yield request

    def parse_drugs_link(self, response):
       
        results = response.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/ul/li/a/@href')

        for link in results:
            print("{}" .format(link.extract()))
            print('-----------')
            print(response.url)
            print('-----------')

        


    