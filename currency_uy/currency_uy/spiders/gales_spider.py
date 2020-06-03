#!/usr/bin/env python3
import scrapy

class GalesSpider(scrapy.Spider):
    name = 'gales'
    start_urls = ['http://www.gales.com.uy/home']

    def parse(self, response):
        rates = response.css('div.cont_cotizaciones table.monedas')
        for tr in rates.css('tr'):
            td = tr.css('td::text').getall()
            yield {
                'name': td[0],
                'buy': td[1],
                'sell': td[2]
            }

