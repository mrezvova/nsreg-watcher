import logging
import re

import scrapy
from nsreg.items import NsregItem

from ..utils import find_price

REGEX_PATTERN = r"[0-9]+[.,\s]?"
EMPTY_PRICE = {
    'pricereg': None,
    'priceprolong': None,
    'pricechange': None,
}

class NsregRegSpider(scrapy.Spider):
    name = 'nsreg_reg'
    allowed_domains = ['www.reg.ru']
    start_urls = ['http://www.reg.ru/']

    def parce(self, response):

        pricereg = response.xpath('//*[@id="content"]/div[3]/div[2]/div[2]/div/div/a/span/span[2]/text()').get()
        pricereg = find_price(REGEX_PATTERN, pricereg)
        
        priceprolong = None

        pricechange = None

        item = NsregItem()
        item['name'] = "ООО «РЕГ.РУ»»"
        price = item.get('price', EMPTY_PRICE)
        price['pricereg'] = pricereg
        price['priceprolong'] = priceprolong
        item['price'] = price

        yield item
