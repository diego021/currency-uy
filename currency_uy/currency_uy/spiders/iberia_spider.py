#!/usr/bin/env python3
import scrapy
from currency_uy.items import CurrencyUyItem

class IberiaSpider(scrapy.Spider):
    name = 'iberia'
    start_urls = ['http://www.cambioiberia.com/']

    def parse(self, response):
        rates = response.css('div.entry.clearfix table')

        for tr in rates.css('tr'):
            item = CurrencyUyItem()
            _values = tr.css('td::text').getall()

            if len(_values) != 3:
                continue

            item['name'] = _values[0]
            item['buy'] = _values[1]
            item['sell'] = _values[2]

            yield item
