#!/usr/bin/env python3
import urllib.request
from bs4 import BeautifulSoup

class GeneralScrapper:
    '''Superclass containing common things to all scrappers'''

    def __init__(self, url):
        r = urllib.request.Request(url)
        r.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0')
        r.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        html = urllib.request.urlopen(r).read()
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

class IndumexScrapper(GeneralScrapper):

    def __init__(self, *args, **kwargs):
        GeneralScrapper.__init__(self, *args, **kwargs)
        self.name = 'Cambio Indumex'
        self.rates_div = self.soup.find('div', attrs={'class': 'rates'}).find('div')

    def scrap_dollar(self):
        assert False, 'Dynamic javascripts load rates!! WORK TO DO'
        #buy = self.rates_div.find('span', id='compraDolar').text # Empty
        #sell = self.rates_div.find('span', id='ventaDolar').text # Empty
        #self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

class IberiaScrapper(GeneralScrapper):

    def __init__(self, *args, **kwargs):
        GeneralScrapper.__init__(self, *args, **kwargs)
        self.name = 'Cambio Iberia'
        self.rates_table = self.soup.find('div', attrs={'class': 'entry clearfix'}).find('table')

    def scrap_dollar(self):
        rates = self.rates_table.find_all('tr')[1].find_all('td')
        buy = self.convert_to_float(rates[2].text)
        sell = self.convert_to_float(rates[3].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

class LaFavoritaScrapper(GeneralScrapper):

    def __init__(self, *args, **kwargs):
        GeneralScrapper.__init__(self, *args, **kwargs)
        self.name = 'La Favorita'
        self.rates_list = self.soup.find('div', attrs={'class': 'row'}).find_all('li', attrs={'class': 'color-cotizacion'})

    def scrap_dollar(self):
        buy = self.convert_to_float(self.rates_list[0].text)
        sell = self.convert_to_float(self.rates_list[1].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

if __name__ == '__main__':
    a = GalesScrapper(url='http://www.gales.com.uy/home/')
    b = VarlixScrapper(url='https://www.varlix.com.uy/')
    c = Cambio18Scrapper(url='https://www.cambio18.com/')
    d = AspenScrapper(url='http://www.aspen.com.uy/sitio/')
    e = MatrizScrapper(url='https://www.cambiomatriz.com.uy/')
    f = IberiaScrapper(url='http://www.cambioiberia.com/') 
    g = LaFavoritaScrapper(url='http://www.lafavorita.com.uy/')
    #f = IndumexScrapper(url='https://www.indumex.com/')
    for i in (a, b, c, d, e, f, g):
        i.scrap_dollar()
        print(i)
