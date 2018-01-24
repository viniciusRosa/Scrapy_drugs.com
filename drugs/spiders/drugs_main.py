# -*- coding: utf-8 -*-
import scrapy
import re
from drugs.items import DrugsSideEffectsItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class DrugsMainSpider(scrapy.Spider):
    name = 'drugs_main'
    allowed_domains = ['drugs.com']
    #Reference link, this shows the side effects of medicines that start with letter 'b'
    first_page_url = ('https://www.drugs.com/sfx-{}.html')

    def __init__(self):
        self.last_page = None

    def start_requests(self):
        """ get results of first page to scrap"""
        request = scrapy.Request(
            url=DrugsMainSpider.first_page_url.format(0),
            callback=self.parse_page,
        )
        yield request

    def parse_page(self, response):
        """ get results of all pages that have will be scraped"""
        #get the last page
        page_list = response.selector.xpath('//div[@class="contentBox"]/div/table/tr')
        if page_list:
            self.last_page = int(response.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/div[2]/table/tr/td[2]/a/text()')[-1].extract())
        else:
            self.last_page = 1

        for page in range(self.last_page):
            request = scrapy.Request(
                url=DrugsMainSpider.first_page_url.format(page),
                callback=self.parse_drugs_link,
                dont_filter = True
            )
            yield request

    def parse_drugs_link(self, response):
        results = response.xpath('/html/body/div[1]/div/div[1]/div[2]/div[1]/div[2]/ul/li/a/@href')

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
        drugs_sfx_ul_li_p = response.selector.xpath('//div[@class="contentBox"]/ul/li/p')
        drugs_sfx_ul_li = response.selector.xpath('//div[@class="contentBox"]/ul/li')
        drugs_sfx_p_sup = response.selector.xpath('//div[@class="contentBox"]/p/sup')
        
        drugs_sfx_item['drug_name'] = drug_name[:-13]

        if drugs_sfx_ul_li_p:
            drugs_sfx_item['drug_side_effects'] = response.xpath('//div[@class="contentBox"]/ul/li/p/text()').extract()
        elif drugs_sfx_ul_li:
            drugs_sfx_item['drug_side_effects'] = response.xpath('//div[@class="contentBox"]/ul/li/text()').extract()
        elif drugs_sfx_p_sup:
            drugs_sfx_item['drug_side_effects'] =response.selector.xpath('//div[@class="contentBox"]/p/sup/../text()').extract()
            
        yield drugs_sfx_item