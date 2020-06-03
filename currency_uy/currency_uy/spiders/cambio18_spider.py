#!/usr/bin/env python3
import scrapy

class Cambio18Spider(scrapy.Spider):
    name = 'cambio18'
    start_urls = ['https://www.cambio18.com/']

    def parse(self, response):
        rates = response.css('div.vc_row.wpb_row.vc_row-fluid.vc_custom_1489540209555.vc_column-gap-20.vc_row-o-content-middle.vc_row-flex') 
        for currency in rates.css('div.wpb_column.vc_column_container.vc_col-sm-3'):
            currency = currency.css('table table')
            td = currency.css('td::text').getall()
            yield {
                'name': currency.css('th::text').get(),
                'buy': td[1],
                'sell': td[-1]
            }

