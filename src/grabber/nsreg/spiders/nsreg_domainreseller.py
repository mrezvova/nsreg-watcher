# -*- coding: utf-8 -*-
import logging
import re

import scrapy
from nsreg.items import NsregItem

from ..utils import find_price
#работает
REGEX_PATTERN = r"([0-9]+)\s+₽.*"
EMPTY_PRICE = {
    'pricereg': None,
    'priceprolong': None,
    'pricechange': None,
}


class NsregBestregSpider(scrapy.Spider):
    name = "nsreg_domainreseller"
    allowed_domains = ["www.domainreseller.ru"]
    start_urls = ["https://domainreseller.ru/domains/"]

    def parse(self, response):
        pricereg = response.xpath('/html/body/section/div/div/div/div/div/div/table/tbody/tr[1]/td[3]/a/text()').get()
        pricereg = find_price(REGEX_PATTERN, pricereg)
        
        priceprolong = response.xpath('/html/body/section/div/div/div/div/div/div/table/tbody/tr[1]/td[4]/a/text()').get()
        priceprolong = find_price(REGEX_PATTERN, priceprolong)

        pricechange = response.xpath('/html/body/section/div/div/div/div/div/div/table/tbody/tr[1]/td[5]/a/text()').get()
        pricechange = find_price(REGEX_PATTERN, pricechange)

        item = NsregItem()
        item['name'] = "ООО «Домэинреселлер»"
        price = item.get('price', EMPTY_PRICE)
        price['pricereg'] = pricereg
        price['priceprolong'] = priceprolong
        price['pricechange'] = pricechange 
        item['price'] = price

        yield item
