# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DrugsSideEffectsItem(scrapy.Item):
    # define the fields for your item here like:
    drug_name = scrapy.Field()
    drug_side_effects = scrapy.Field()

class DiseaseMedicinesItem(scrapy.Item):
    # define the fields for your item here like:
    disease = scrapy.Field()
    medicine = scrapy.Field()
    # amount = scrapy.Field()
    # url = scrapy.Field()
