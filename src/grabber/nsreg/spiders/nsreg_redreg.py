import scrapy
from ..utils import find_price
REGEX_PATTERN = r"([0-9]+[.,\s])?руб"

class NsregRedregSpider(scrapy.Spider):
    name = 'nsreg_redreg'
    allowed_domains = ['red-reg.ru']
    start_urls = ['https://www.red-reg.ru/price/']

    def parse(self, response):
        pricereg = response.xpath('//article[@class="b-prices__item b-section"]/div/table/tr[5]/td[@class="b-table__cell"]/text()').get()
        pricereg = find_price(REGEX_PATTERN, pricereg)
        priceprolong = response.xpath('//article[@class="b-prices__item b-section"]/div/table/tr[5]/td[@class="b-table__cell b-table__cell_last"]/text()').get()
        priceprolong = find_price(REGEX_PATTERN, priceprolong)
        print ('!!!!!!!!!! AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH I AM RUNNING!!!!!!!!!!!!!!!!!!!!!!!!!')
        item = NsregItem()
        item['name'] = "ООО «Редрег»"
        price = item.get('price', EMPTY_PRICE)
        price['pricereg'] = pricereg
        price['priceprolong'] = priceprolong
        item['price'] = price

        yield item
