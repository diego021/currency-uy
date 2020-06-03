#!/usr/bin/env python3
import scrapy
from currency_uy.items import CurrencyUyItem


class MatrizSpider(scrapy.Spider):
    name = 'matriz'
    start_urls = ['https://www.cambiomatriz.com.uy/']

    def parse(self, response):
        rates = response.css('div.cont.cotizaciones table')[0]
        for tr in rates.css('tr'):
            item = CurrencyUyItem()
            _values = tr.css('td.ff_arial.fuente_num::text').getall()

            item['name'] = tr.css('td.nom::text').get().strip()
            item['buy'] = _values[0]
            item['sell'] = _values[-1]

            yield item
