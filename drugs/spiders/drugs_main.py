# -*- coding: utf-8 -*-
import scrapy
from drugs.items import DrugsSideEffectsItem


class DrugsMainSpider(scrapy.Spider):
    name = 'drugs_main'
    allowed_domains = ['drugs.com']
    first_page_url = ('https://www.drugs.com/sfx-a{}.html')

    def __init__(self):
        self.last_page = None

    """ get results of first page """
    def start_requests(self):
        request = scrapy.Request(
            url=DrugsMainSpider.first_page_url.format(0),
            callback=self.parse_page,
        )
        yield request

    """ get results of all pages """
    def parse_page(self, response):
        self.last_page = int(response.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[2]/table/tr/td[2]/a/text()')[-1].extract())

        for page in range(1, 2):
        #for page in range(1, self.last_page + 1):
            request = scrapy.Request(
                url=DrugsMainSpider.first_page_url.format(page),
                callback=self.parse_drugs_link,
            )
            yield request

    def parse_drugs_link(self, response):
        results = response.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/ul/li/a/@href')
        #results = response.css('.column-list-2 li a::attr(href)').extract()

        for drug_link in results:
            url_drug = 'https://www.drugs.com' + drug_link.extract()
            #print(url_drug)
            request = scrapy.Request(
                url=url_drug,
                callback=self.parse_drugs_detail_description
            )
            yield request

    def parse_drugs_detail_description(self, response):
        drugs_sfx_item = DrugsSideEffectsItem()
        drug_name = response.css('h1::text').extract_first()
        drugs_sfx = response.css('.contentBox ul:not(.more-resources-list)>li::text').extract()

        drugs_sfx_item['drug_name'] = drug_name[:-13]
        drugs_sfx_item['drug_side_effects'] = drugs_sfx
        yield drugs_sfx_item