#!/usr/bin/env python3
import scrapy
from currency_uy.items import CurrencyUyItem


class Cambio18Spider(scrapy.Spider):
    name = 'cambio18'
    start_urls = ['https://www.cambio18.com/']

    def parse(self, response):
        rates = response.css('div.vc_row.wpb_row.vc_row-fluid.vc_custom_1489540209555.vc_column-gap-20.vc_row-o-content-middle.vc_row-flex')
        for currency in rates.css('div.wpb_column.vc_column_container.vc_col-sm-3'):
            item = CurrencyUyItem()
            currency = currency.css('table table')
            td = currency.css('td::text').getall()

            item['name'] = currency.css('th::text').get()
            item['buy'] = td[1]
            item['sell'] = td[-1]

            yield item
