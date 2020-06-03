#!/usr/bin/env python3
import scrapy

class AspenSpider(scrapy.Spider):
    name = 'aspen'
    start_urls = ['http://www.aspen.com.uy/sitio/']

    def parse(self, response):
        rates = response.css('div.md-cotizaciones')
        for div in rates.css('div.row-fluid div'):
            for tr in div.css('tr.bd'):
                values = tr.css('td.valor::text').getall()
                yield {
                    'name': tr.css('td.moneda::text').get(),
                    'buy': values[0],
                    'sell': values[1]
                }

