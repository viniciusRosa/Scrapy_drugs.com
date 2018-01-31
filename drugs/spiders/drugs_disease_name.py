# -*- coding: utf-8 -*-
import scrapy
import re
from drugs.items import DiseaseMedicinesItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class DrugsDiseaseNameSpider(scrapy.Spider):
    name = 'drugs_disease_name'
    allowed_domains = ['drugs.com']
    first_page_url = ('https://www.drugs.com/condition/a.html')

    def __init__(self):
        self.condition_name = None
        self.dict_result = {}

    """ get results of first page """
    def start_requests(self):
        request = scrapy.Request(
            url=DrugsDiseaseNameSpider.first_page_url,
            callback=self.parse_diseage_link,
        )
        yield request
   
    """ get the pages that should be scraped """
    def parse_diseage_link(self, response):
        results = response.xpath('//div[@class="contentBox"]/ul[@class="column-list-2"]/li/a/@href')

        for disease_link in results:           
            url_disease = 'https://www.drugs.com' + disease_link.extract()           
            request = scrapy.Request(
                url=url_disease,
                callback=self.parse_page,
            )
            yield request

    """ get results of all pages """
    def parse_page(self, response):
        diseaseMedicineItem = DiseaseMedicinesItem()
        url = self.configure_url(response.url)
        pages = 1

        if response.selector.xpath('//div[@class="contentBox"]/div[@id="conditionBoxWrap"]'):
            if response.selector.xpath('//div[@class="contentBox"]/div[@id="conditionBoxWrap"]/div[@class="paging-list paging-list-condition-list"]'):
                pages = int(response.css('td.paging-list-index:nth-child(2) a::text')[-1].extract())
       
            for page in range(1, pages + 1):

                url_page = '{}?page_number={}' .format(url, page)
                print('\n{}' .format(url_page))
                request = scrapy.Request(
                    url=url_page,
                    callback= self.parse_medications,
                    dont_filter = True
                )
                yield request
        else:
            condition_name = response.css('h1::text').extract_first()
            self.dict_result[condition_name[19:]] = ""


        for num in range(0, len(self.dict_result)):
            item = self.dict_result.popitem()
            print('{} => {}' .format(item[0], item[1]))

            diseaseMedicineItem['disease'] = item[0]
            diseaseMedicineItem['medicine'] = item[1]
            diseaseMedicineItem['amount'] = len(item[1])

            yield diseaseMedicineItem

    def parse_medications(self, response):

        condition_name = response.css('h1::text').extract_first()
        medications = response.xpath('//div[@class="contentBox"]/div[@id="conditionBoxWrap"]/table[@class="condition-table"]/tbody/tr/td/span/a[@class="condition-table__drug-name__link"]/text()')
        

        if condition_name[19:] in self.dict_result:
            for medication in medications:
                self.dict_result[condition_name[19:]].append(medication.extract())
        else:
            self.dict_result[condition_name[19:]] = medications.extract()
    
    def configure_url(self, url):
        cut_point = url.find('html')
        return url[:cut_point + 4]
