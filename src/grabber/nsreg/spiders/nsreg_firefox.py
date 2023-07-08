import logging
import re

import scrapy
from nsreg.items import NsregItem

from ..utils import find_price

REGEX_PATTERN = r"([0-9]+)"
EMPTY_PRICE = {
    'pricereg': None,
    'priceprolong': None,
    'pricechange': None,
}

def xpath(index: int) -> str:
    return f'/html/body/section/div/div/div/div[@class="border rounded"]/div[{index}]/div[2]/span/text()'


class NsregFirefoxSpider(scrapy.Spider):
    name = "nsreg_firefox"
    allowed_domains = ["firefox.ru"]
    start_urls = ["https://firefox.ru/site/tariffs"]

    def parse(self, response):
        pricereg = find_price(REGEX_PATTERN, response.xpath(xpath(1)).get())
        priceprolong = find_price(REGEX_PATTERN, response.xpath(xpath(2)).get())
        pricechange = find_price(REGEX_PATTERN, response.xpath(xpath(3)).get())

        item = NsregItem()
        item['name'] = "ООО «ФАЕРФОКС»"
        price = item.get('price', EMPTY_PRICE)
        price['pricereg'] = pricereg
        price['priceprolong'] = priceprolong
        price['pricechange'] = pricechange 
        item['price'] = price

        yield item
