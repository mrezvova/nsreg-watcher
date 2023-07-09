import scrapy

from ..utils_spider import moscow_tariffs

REGEX_PATTERN = r"([0-9]+)"
name = "ООО «ФАЕРФОКС»"


class NsregFirefoxSpider(scrapy.Spider):
    name = "nsreg_firefox"
    allowed_domains = ["firefox.ru"]
    start_urls = ["https://firefox.ru/site/tariffs"]

    def parse(self, response):
        item = moscow_tariffs(self, response, REGEX_PATTERN, name)
        yield item
