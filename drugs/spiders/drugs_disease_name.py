# -*- coding: utf-8 -*-
import scrapy
import re
from drugs.items import DrugsSideEffectsItem


class DrugsDiseaseNameSpider(scrapy.Spider):
    name = 'drugs_diseage_name'
    allowed_domains = ['drugs.com']
    first_page_url = ('https://www.drugs.com/sfx-a{}.html')

    def __init__(self):
        self.last_page = None

    """ get results of first page """
    def start_requests(self):
        request = scrapy.Request(
            url=DrugsDiseaseNameSpider.first_page_url.format(0),
            callback=self.parse_page,
        )
        yield request

    """ get results of all pages """
    def parse_page(self, response):
        self.last_page = int(response.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[2]/table/tr/td[2]/a/text()')[-1].extract())

        for page in range(0, self.last_page):
            request = scrapy.Request(
                url=DrugsDiseaseNameSpider.first_page_url.format(page),
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

    # def parse_drugs_detail_description(self, response):
    #     drugs_sfx_item = DrugsSideEffectsItem()
    #     drug_name = response.css('h1::text').extract_first()
    #     drugs_sfx = response.css('.contentBox ul:not(.more-resources-list)>li::text').extract()

    #     drugs_sfx_item['drug_name'] = drug_name[:-13]
    #     drugs_sfx_item['drug_side_effects'] = drugs_sfx
    #     yield drugs_sfx_item

    def parse_drugs_detail_description(self, response):
        drugs_sfx_item = DrugsSideEffectsItem()
        drug_name = response.css('h1::text').extract_first()
        drugs_sfx = response.xpath('//div[@class="contentBox"]/ul/li')

        drugs_sfx_item['drug_name'] = drug_name[:-13]

        if drugs_sfx.css('p'):
            drugs_sfx_item['drug_side_effects'] = response.xpath('//div[@class="contentBox"]/ul/li/p/text()').extract()
        else:
            drugs_sfx_item['drug_side_effects'] = response.xpath('//div[@class="contentBox"]/ul/li/text()').extract()
        
        yield drugs_sfx_item