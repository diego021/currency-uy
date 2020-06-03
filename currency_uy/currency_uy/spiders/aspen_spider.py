#!/usr/bin/env python3
import scrapy
from currency_uy.items import CurrencyUyItem


class AspenSpider(scrapy.Spider):
    name = 'aspen'
    start_urls = ['http://www.aspen.com.uy/sitio/']

    def parse(self, response):
        rates = response.css('div.md-cotizaciones')

        for div in rates.css('div.row-fluid div'):
            for tr in div.css('tr.bd'):
                item = CurrencyUyItem()
                _values = tr.css('td.valor::text').getall()

                item['name'] = tr.css('td.moneda::text').get()
                item['buy'] = _values[0]
                item['sell'] = _values[1]

                yield item
