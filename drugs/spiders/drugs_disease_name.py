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
        self.diseage_medication_name = []

    """ get results of first page """
    def start_requests(self):
        request = scrapy.Request(
            url=DrugsDiseaseNameSpider.first_page_url.format(),
            callback=self.parse_diseage_link,
        )
        yield request
   
    def parse_diseage_link(self, response):
        results = response.xpath('//div[@class="contentBox"]/ul[@class="column-list-2"]/li/a/@href')

        for disease_link in results:           
            url_disease = 'https://www.drugs.com' + disease_link.extract()           
            request = scrapy.Request(
                url=url_disease,
                callback=self.parse_page,
                dont_filter = True
            )
            yield request

    """ get results of all pages """
    def parse_page(self, response):
        condition_name = response.css('h1::text').extract_first()
        self.condition_name =  condition_name[19:]
        medications = []
        pages = None
        if response.selector.xpath('//div[@class="contentBox"]/div[@id="conditionBoxWrap"]'):
            if response.selector.xpath('//div[@class="contentBox"]/div[@id="conditionBoxWrap"]/div[@class="paging-list paging-list-condition-list"]'):
                pages = int(response.css('td.paging-list-index:nth-child(2) a::text')[-1].extract())
            else:
                pages = 1

            for page in range(1, pages + 1):
                try:
                    url_page = '{}?page_number={}' .format(response.url, page)
                    print('\n{}' .format(url_page))
                    request = scrapy.Request(
                        url=url_page,
                        callback= self.parse_medications(response, medications),
                        dont_filter = True
                    )
                except Exception as e:
                    print("URL {}, generic error : {}".format(response.url, e))
                    return               
        else:
            medications.append('none')

        diseaseMedicineItem = DiseaseMedicinesItem()

        print('------------------------------------')
        print('{} \n {}' .format(condition_name[19:], medications))
        print('------------------------------------')

        diseaseMedicineItem['disease'] = condition_name[19:]
        diseaseMedicineItem['medicine'] = medications

        yield diseaseMedicineItem
   
    def parse_medications(self, response, medications):
        
        select_medication = response.xpath('//div[@class="contentBox"]/div[@id="conditionBoxWrap"]/table[@class="condition-table"]/tbody/tr/td/span/a[@class="condition-table__drug-name__link"]/text()')

        for item in select_medication:
            try:
               self.diseage_medication_name.append(item)
               medications.append(item.extract())
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

