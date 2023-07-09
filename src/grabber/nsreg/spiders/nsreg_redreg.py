import scrapy
from nsreg.items import NsregItem

from ..utils_spiders import moscow_price

REGEX_PATTERN = r"([0-9]+[.,\s])?руб"
EMPTY_PRICE = {
    'pricereg': None,
    'priceprolong': None,
    'pricechange': None,
}

class NsregRedregSpider(scrapy.Spider):
    name = 'nsreg_redreg'
    allowed_domains = ['red-reg.ru']
    start_urls = ['https://www.red-reg.ru/price/']

    def parse(self, response):
        item = moscow_price(self, response, REGEX_PATTERN, "ООО «Редрег»")

        yield item
