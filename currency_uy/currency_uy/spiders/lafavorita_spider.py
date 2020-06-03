#!/usr/bin/env python3
import scrapy

class IberiaSpider(scrapy.Spider):
    name = 'lafavorita'
    start_urls = ['http://www.lafavorita.com.uy/']

    def parse(self, response):
        rates = response.css('div.row ul.course-block')
        for ul in rates:
            name = ul.css('img::attr(src)').get().split('/')[-1][:-5]
            values = ul.css('li.color-cotizacion::text').getall()

            yield {
                'name': name,
                'buy': values[0],
                'sell': values[1]
            }
