#!/usr/bin/env python3
import scrapy
from currency_uy.items import CurrencyUyItem


class LafavoritaSpider(scrapy.Spider):
    name = 'lafavorita'
    start_urls = ['http://www.lafavorita.com.uy/']

    def parse(self, response):
        rates = response.css('div.row ul.course-block')
        for ul in rates:
            item = CurrencyUyItem()
            _name = ul.css('img::attr(src)').get().split('/')[-1][:-5]
            _values = ul.css('li.color-cotizacion::text').getall()

            item['name'] = _name
            item['buy'] = _values[0]
            item['sell'] = _values[1]

            yield item
