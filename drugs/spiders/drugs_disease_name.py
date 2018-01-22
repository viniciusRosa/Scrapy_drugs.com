# -*- coding: utf-8 -*-
import scrapy
import re
from drugs.items import DrugsSideEffectsItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


class DrugsDiseaseNameSpider(scrapy.Spider):
    name = 'drugs_disease_name'
    allowed_domains = ['drugs.com']
    first_page_url = ('https://www.drugs.com/condition/{}.html')

    def __init__(self):
        self.condition_name = None

    """ get results of first page """
    def start_requests(self):
        request = scrapy.Request(
            url=DrugsDiseaseNameSpider.first_page_url.format('a'),
            callback=self.parse_diseage_link,
        )
        yield request
   

    def parse_diseage_link(self, response):
        results = response.xpath('//div[@class="contentBox"]/ul[@class="column-list-2"]/li/a/@href')

        for disease_link in results:           
            url_disease = 'https://www.drugs.com' + disease_link.extract()           
            request = scrapy.Request(
                url=url_disease,
                callback=self.parse_page
            )
            yield request



     

    """ get results of all pages """
    def parse_page(self, response):
        condition_name = response.css('h1::text').extract_first()
        self.condition_name =  condition_name[19:]
        diseage_medication_name = []
        if response.selector.xpath('//div[@class="contentBox"]/div[@id="conditionBoxWrap"]'):
            self.extract_medications(response, diseage_medication_name)



    def extract_medications(self, response, diseage_medication_name):
        # print('{} \n' .format(response.url))
        pages = 1
        if response.selector.xpath('//div[@class="contentBox"]/div[@id="conditionBoxWrap"]/div[@class="paging-list paging-list-condition-list"]'):
            pages = int(response.css('td.paging-list-index:nth-child(2) a::text')[-1].extract())

        for page in range(1, pages + 1):
            url_page = '{}?page_number={}' .format(response.url, page)
            print('\n{} -> {}\n' .format(url_page, self.condition_name))
            # request = scrapy.Request(
            #     url=url_page,
            #     callback=
            # )
    

#     def parse_drugs_detail_description(self, response):
#         drugs_sfx_item = DrugsSideEffectsItem()
#         drug_name = response.css('h1::text').extract_first()
#         drugs_sfx = response.xpath('//div[@class="contentBox"]/ul/li')

#         drugs_sfx_item['drug_name'] = drug_name[:-13]

#         if drugs_sfx.css('p'):
#             drugs_sfx_item['drug_side_effects'] = response.xpath('//div[@class="contentBox"]/ul/li/p/text()').extract()
#         else:
#             drugs_sfx_item['drug_side_effects'] = response.xpath('//div[@class="contentBox"]/ul/li/text()').extract()
        
#         yield drugs_sfx_item