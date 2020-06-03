#!/usr/bin/env python3
import scrapy

class VarlixSpider(scrapy.Spider):
    name = 'varlix'
    start_urls = ['https://www.varlix.com.uy/']

    def parse(self, response):
        rates = response.css('div.exchange')
        for currency in rates.css('div.exchange-line'):
            yield {
                'name': currency.css('div.currency::text').get(),
                'buy': currency.css('div.buy::text').get(),
                'sell': currency.css('div.sell::text').get()
            }

