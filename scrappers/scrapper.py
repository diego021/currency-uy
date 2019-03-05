#!/usr/bin/env python3
import urllib.request
from bs4 import BeautifulSoup

class GeneralScrapper:
    '''Superclass containing common things to all scrappers'''

    def __init__(self, url):
        html = urllib.request.urlopen(url).read()
        self.soup = BeautifulSoup(html, 'html.parser')
        self.name = 'General Scrapper'
        self.rates = {}

    def __str__(self):
        return '{name}: {rates}'.format(name=self.name, rates=self.rates)

    @staticmethod
    def convert_to_float(text):
        return float(text.replace(',', '.'))

class GalesScrapper(GeneralScrapper):

    def __init__(self, *args, **kwargs):
        GeneralScrapper.__init__(self, *args, **kwargs)
        self.name = 'Cambio Gales'
        self.rates_table = self.soup.find('div', attrs={'class': 'cont_cotizaciones'})

    def scrap_dollar(self):
        rates = self.rates_table.find('tr').find_all('td')
        buy = self.convert_to_float(rates[1].text)
        sell = self.convert_to_float(rates[2].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

class VarlixScrapper(GeneralScrapper):

    def __init__(self, *args, **kwargs):
        GeneralScrapper.__init__(self, *args, **kwargs)
        self.name = 'Cambio Varlix'
        self.rates_div = self.soup.find('div', attrs={'class': 'exchange'})

    def scrap_dollar(self):
        buy = self.rates_div.find('div', attrs={'class': 'buy'})
        buy = self.convert_to_float(buy.text)
        sell = self.rates_div.find('div', attrs={'class': 'sell'})
        sell = self.convert_to_float(sell.text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

class Cambio18Scrapper(GeneralScrapper):

    def __init__(self, *args, **kwargs):
        GeneralScrapper.__init__(self, *args, **kwargs)
        self.name = 'Cambio 18'
        self.rates_div = self.soup.find('div', attrs={'class': 'clearfix control-page-smallHeader'}).find('div')

    def scrap_dollar(self):
        rates = self.rates_div.find('div').find('table').find_all('td')
        buy = self.convert_to_float(rates[1].text)
        sell = self.convert_to_float(rates[3].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

class AspenScrapper(GeneralScrapper):

    def __init__(self, *args, **kwargs):
        GeneralScrapper.__init__(self, *args, **kwargs)
        self.name = 'Cambio Aspen'
        self.rates_table = self.soup.find('div', attrs={'class': 'bd fx'}).find('table')

    def scrap_dollar(self):
        rates = self.rates_table.find_all('tr', attrs={'class': 'bd'})[1].find_all('td')
        buy = self.convert_to_float(rates[1].text)
        sell = self.convert_to_float(rates[2].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

class MatrizScrapper(GeneralScrapper):

    def __init__(self, *args, **kwargs):
        GeneralScrapper.__init__(self, *args, **kwargs)
        self.name = 'Cambio Matriz'
        self.rates_table = self.soup.find('div', attrs={'class': 'cont cotizaciones'}).find('table')

    def scrap_dollar(self):
        rates = self.rates_table.find('tr').find_all('td')
        buy = self.convert_to_float(rates[2].text)
        sell = self.convert_to_float(rates[4].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

if __name__ == '__main__':
    a = GalesScrapper(url='http://www.gales.com.uy/home/')
    b = VarlixScrapper(url='https://www.varlix.com.uy/')
    c = Cambio18Scrapper(url='https://www.cambio18.com/')
    d = AspenScrapper(url='http://www.aspen.com.uy/sitio/')
    e = MatrizScrapper(url='https://www.cambiomatriz.com.uy/')
    for i in (a, b, c, d, e):
        i.scrap_dollar()
        print(i)
