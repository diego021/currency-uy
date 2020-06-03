#!/usr/bin/env python3
import datetime
import scrapy
from currency_uy.items import CurrencyUyItem


class IndumexSpider(scrapy.Spider):
    name = 'indumex'
    currencies = {}
    start_urls = ['https://www.indumex.com/Umbraco/api/Pizarra/getMonedas']
    today = datetime.datetime.now().strftime('%d%m%Y')

    def parse(self, response):
        response.selector.register_namespace('i', 'http://schemas.datacontract.org/2004/07/IndumexPortal')
        currencies = response.xpath('/i:ArrayOfMonedas/i:Monedas')

        for c in currencies:
            id_currency, name = c.xpath('./i:IdMoneda/text()').get(), c.xpath('./i:Nombre/text()').get()
            IndumexSpider.currencies[id_currency] = name

        yield scrapy.Request(f'https://www.indumex.com/Umbraco/api/Pizarra/Cotizaciones?fecha={IndumexSpider.today}', callback=self.parse_rates)

    def parse_rates(self, response):
        response.selector.register_namespace('i', 'http://schemas.datacontract.org/2004/07/IndumexPortal.Models')

        for rate in response.xpath('/i:ArrayOfPizarraModel/i:PizarraModel'):
            item = CurrencyUyItem()
            item['name'] = IndumexSpider.currencies[rate.xpath('./i:Moneda/text()').get()]
            item['buy'] = rate.xpath('./i:Compra/text()').get()
            item['sell'] = rate.xpath('./i:Venta/text()').get()
            yield item
