# -*- coding: utf-8 -*-
import logging
import re

import scrapy
from nsreg.items import NsregItem

from ..utils import find_price

REGEX_PATTERN = r"([0-9]+[.,\s])?руб"
EMPTY_PRICE = {
    'pricereg': None,
    'priceprolong': None,
    'pricechange': None,
}
class Nsreg4itSpider(scrapy.Spider):
    name = "nsreg_elvistelekom"
    allowed_domains = ["www.getname.ru"]
    start_urls = ["http://www.getname.ru/reg/price"]

    def parse(self, response):
        pricereg = response.xpath('/html/body/table/tr[6]/td[2]/table[2]/tr[3]/td[2]/text()').get()
        pricereg = find_price(REGEX_PATTERN, pricereg)

        priceprolong = response.xpath('/html/body/table/tr[6]/td[2]/table[2]/tr[5]/td[2]/text()').get()
        priceprolong = find_price(REGEX_PATTERN, priceprolong)

        pricechange = response.xpath('/html/body/table/tr[6]/td[2]/table[2]/tr[7]/td[2]/text()').get()
        pricechange = find_price(REGEX_PATTERN, pricechange.lower())

        item = NsregItem()
        item['name'] = "ООО «Элвис-Телеком»"
        price = item.get('price', EMPTY_PRICE)
        price['pricereg'] = pricereg
        price['priceprolong'] = priceprolong
        price['pricechange'] = pricechange
        item['price'] = price

        yield item
