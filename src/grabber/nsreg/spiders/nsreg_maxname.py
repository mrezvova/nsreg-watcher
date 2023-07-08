import scrapy
from nsreg.items import NsregItem

from ..utils import find_price

REGEX_PATTERN = r"([0-9]+[.,\s])?руб"
EMPTY_PRICE = {
    "pricereg": None,
    "priceprolong": None,
    "pricechange": None,
}


class NsregMaxnameSpider(scrapy.Spider):
    name = "nsreg_maxname"
    allowed_domains = ["maxname.ru"]
    start_urls = ["https://maxname.ru/domains/"]

    def parse(self, response):
        pricereg = response.xpath(
            "/html/body/div[2]/div/section/div/table[1]/tbody/tr[1]/td[2]/text()"
        ).get()
        pricereg = find_price(REGEX_PATTERN, pricereg)

        priceprolong = response.xpath(
            "/html/body/div[2]/div/section/div/table[1]/tbody/tr[3]/td[2]/text()"
        ).get()
        priceprolong = find_price(REGEX_PATTERN, priceprolong)

        pricechange = response.xpath(
            "/html/body/div[2]/div/section/div/table[1]/tbody/tr[5]/td[2]/text()"
        ).get()
        pricechange = find_price(REGEX_PATTERN, pricechange)

        item = NsregItem()
        item["name"] = "ООО «МаксНейм»"
        price = item.get("price", EMPTY_PRICE)
        price["pricereg"] = pricereg
        price["priceprolong"] = priceprolong
        item["price"] = price

        yield item
