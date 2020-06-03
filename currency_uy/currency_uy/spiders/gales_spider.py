#!/usr/bin/env python3
import scrapy
from currency_uy.items import CurrencyUyItem

class GalesSpider(scrapy.Spider):
    name = 'gales'
    start_urls = ['http://www.gales.com.uy/home']

    def parse(self, response):
        rates = response.css('div.cont_cotizaciones table.monedas')
        for tr in rates.css('tr'):
            item = CurrencyUyItem()
            td = tr.css('td::text').getall()

            item['name'] = td[0]
            item['buy'] = td[1]
            item['sell'] = td[2]

            yield item
