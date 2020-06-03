#!/usr/bin/env python3
import scrapy

class IberiaSpider(scrapy.Spider):
    name = 'iberia'
    start_urls = ['http://www.cambioiberia.com/']

    def parse(self, response):
        rates = response.css('div.entry.clearfix table')

        for tr in rates.css('tr'):
            values = tr.css('td::text').getall()

            if len(values) != 3:
                continue

            yield {
                'name': values[0],
                'buy': values[1],
                'sell': values[2]
            }
