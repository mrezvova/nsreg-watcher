import logging
import re

import scrapy
from nsreg.items import NsregItem

from ..utils import find_price

REGEX_PATTERN = r".*(([0-9]*)?[0-9]{3})\s+руб."
REGEX_CHANGE_PATTERN = r".*[А-я]*"
EMPTY_PRICE = {
    'pricereg': None,
    'priceprolong': None,
    'pricechange': None,
}


class NsregCetisregSpider(scrapy.Spider):
    name = "nsreg_cetisreg"
    allowed_domains = ["www.cetis-reg.ru"]
    start_urls = ["https://www.cetis-reg.ru/price/"]

    def parse(self, response):
        pricereg = response.xpath(
            '/html/body/div[1]/div[3]/article/section/table[1]/tr/td[1]/article[1]/div/table/tr[4]/td[2]/text()'
        ).get()
        pricereg = find_price(REGEX_PATTERN, pricereg)

        priceprolong = response.xpath(
            '/html/body/div[1]/div[3]/article/section/table[1]/tr/td[1]/article[1]/div/table/tr[4]/td[3]/text()').get()
        priceprolong = find_price(REGEX_PATTERN, priceprolong)

        pricechange = response.xpath(
            '/html/body/div[1]/div[3]/article/section/table[2]/tr/td[1]/article[2]/div/table/tr[10]/td[2]/text()').get()
        pricechange = find_price(REGEX_CHANGE_PATTERN, pricechange)

        item = NsregItem()
        item['name'] = "ООО «ЦЭТИС»"
        price = item.get('price', EMPTY_PRICE)
        price['pricereg'] = pricereg
        price['priceprolong'] = priceprolong
        price['pricechange'] = pricechange
        item['price'] = price

        yield item
