#!/usr/bin/env python3
import scrapy
from currency_uy.items import CurrencyUyItem


class VarlixSpider(scrapy.Spider):
    name = 'varlix'
    start_urls = ['https://www.varlix.com.uy/']

    def parse(self, response):
        rates = response.css('div.exchange')
        for currency in rates.css('div.exchange-line'):
            item = CurrencyUyItem()
            item['name'] = currency.css('div.currency::text').get()
            item['buy'] = currency.css('div.buy::text').get()
            item['sell'] = currency.css('div.sell::text').get()
            yield item
