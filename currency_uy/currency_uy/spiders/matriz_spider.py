#!/usr/bin/env python3
import scrapy

class MatrizSpider(scrapy.Spider):
    name = 'matriz'
    start_urls = ['https://www.cambiomatriz.com.uy/']

    def parse(self, response):
        rates = response.css('div.cont.cotizaciones table')[0]
        for tr in rates.css('tr'):
            values = tr.css('td.ff_arial.fuente_num::text').getall()
            yield {
                'name': tr.css('td.nom::text').get().strip(),
                'buy': values[0],
                'sell': values[-1]
            }
