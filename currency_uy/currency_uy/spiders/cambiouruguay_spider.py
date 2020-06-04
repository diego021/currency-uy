#!/usr/bin/env python3
import scrapy
from currency_uy.items import CurrencyUyItem


class UruguaySpider(scrapy.Spider):
    name = 'cambio_uruguay'
    start_urls = ['https://cambiouruguay.com.uy/']

    def parse(self, response):
        rates = response.css('table.pure-table.pure-table-horizontal')

        for tr in rates.css('tr'):
            item = CurrencyUyItem()
            _values = tr.css('td::text').getall()

            if not _values:
                continue

            item['name'] = _values[0]
            item['buy'] = _values[1]
            item['sell'] = _values[2]

            yield item
