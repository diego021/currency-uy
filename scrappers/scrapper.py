#!/usr/bin/env python3
import dataclasses
import urllib.request
from abc import ABC, abstractmethod
from decimal import Decimal

from bs4 import BeautifulSoup


@dataclasses.dataclass
class Rate:
    buy: Decimal
    sell: Decimal
    # TODO


class ScrapperBase(ABC):
    """Base scrapper class."""

    def __init__(self, url, name=None):
        self.name = name
        self.url = url
        self.rates = {}
        self._soup = None

    @abstractmethod
    def prepare(self):
        _accept = (
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        )
        _user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/'
            '20100101 Firefox/60.0'
        )

        r = urllib.request.Request(self.url)
        r.add_header('Accept', _accept)
        r.add_header('User-Agent', _user_agent)

        html = urllib.request.urlopen(r).read()
        self._soup = BeautifulSoup(html, 'html.parser')

    @abstractmethod
    def scrap_dollar(self):
        assert False, 'Must implement this method'

    @staticmethod
    def to_decimal(text_value):
        return Decimal(text_value.replace(',', '.')).quantize(Decimal('0.01'))

    def __str__(self):
        return f'{self.name}: {self.rates}'

    def _persist(self):
        pass  # TODO


class GalesScrapper(ScrapperBase):

    def __init__(self, *args, **kwargs):
        ScrapperBase.__init__(self, *args, **kwargs, name='Cambio Gales')

    def prepare(self):
        ScrapperBase.prepare(self)
        self.rates_table = self._soup.find(
            'div', attrs={'class': 'cont_cotizaciones'}
        )

    def scrap_dollar(self):
        rates = self.rates_table.find('tr').find_all('td')
        buy = self.to_decimal(rates[1].text)
        sell = self.to_decimal(rates[2].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})


class VarlixScrapper(ScrapperBase):

    def __init__(self, *args, **kwargs):
        ScrapperBase.__init__(self, *args, **kwargs, name='Cambio Varlix')

    def prepare(self):
        ScrapperBase.prepare(self)
        self.rates_div = self._soup.find('div', attrs={'class': 'exchange'})

    def scrap_dollar(self):
        buy = self.rates_div.find('div', attrs={'class': 'buy'})
        buy = self.to_decimal(buy.text)
        sell = self.rates_div.find('div', attrs={'class': 'sell'})
        sell = self.to_decimal(sell.text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})


class Cambio18Scrapper(ScrapperBase):

    def __init__(self, *args, **kwargs):
        ScrapperBase.__init__(self, *args, **kwargs, name='Cambio 18')

    def prepare(self):
        ScrapperBase.prepare(self)
        self.rates_div = self._soup.find(
            'div', attrs={'class': 'clearfix control-page-smallHeader'}
        ).find('div')

    def scrap_dollar(self):
        rates = self.rates_div.find('div').find('table').find_all('td')
        buy = self.to_decimal(rates[1].text)
        sell = self.to_decimal(rates[3].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})


class AspenScrapper(ScrapperBase):

    def __init__(self, *args, **kwargs):
        ScrapperBase.__init__(self, *args, **kwargs, name='Cambio Aspen')

    def prepare(self):
        ScrapperBase.prepare(self)
        self.rates_table = self._soup.find(
            'div', attrs={'class': 'bd fx'}
        ).find('table')

    def scrap_dollar(self):
        rates = self.rates_table.find_all(
            'tr', attrs={'class': 'bd'}
        )[1].find_all('td')
        buy = self.to_decimal(rates[1].text)
        sell = self.to_decimal(rates[2].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})


class MatrizScrapper(ScrapperBase):

    def __init__(self, *args, **kwargs):
        ScrapperBase.__init__(self, *args, **kwargs, name='Cambio Matriz')

    def prepare(self):
        ScrapperBase.prepare(self)
        self.rates_table = self._soup.find(
            'div', attrs={'class': 'cont cotizaciones'}
        ).find('table')

    def scrap_dollar(self):
        rates = self.rates_table.find('tr').find_all('td')
        buy = self.to_decimal(rates[2].text)
        sell = self.to_decimal(rates[4].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})


class IberiaScrapper(ScrapperBase):

    def __init__(self, *args, **kwargs):
        ScrapperBase.__init__(self, *args, **kwargs, name='Cambio Iberia')

    def prepare(self):
        ScrapperBase.prepare(self)
        self.rates_table = self._soup.find(
            'div', attrs={'class': 'entry clearfix'}
        ).find('table')

    def scrap_dollar(self):
        rates = self.rates_table.find_all('tr')[1].find_all('td')
        buy = self.to_decimal(rates[2].text)
        sell = self.to_decimal(rates[3].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})


class LaFavoritaScrapper(ScrapperBase):

    def __init__(self, *args, **kwargs):
        ScrapperBase.__init__(self, *args, **kwargs, name='La Favorita')

    def prepare(self):
        ScrapperBase.prepare(self)
        self.rates_list = self._soup.find(
            'div', attrs={'class': 'row'}
        ).find_all('li', attrs={'class': 'color-cotizacion'})

    def scrap_dollar(self):
        buy = self.to_decimal(self.rates_list[0].text)
        sell = self.to_decimal(self.rates_list[1].text)
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})


if __name__ == '__main__':
    a = GalesScrapper(url='http://www.gales.com.uy/home/')
    b = VarlixScrapper(url='https://www.varlix.com.uy/')
    c = Cambio18Scrapper(url='https://www.cambio18.com/')
    d = AspenScrapper(url='http://www.aspen.com.uy/sitio/')
    e = MatrizScrapper(url='https://www.cambiomatriz.com.uy/')
    f = IberiaScrapper(url='http://www.cambioiberia.com/')
    g = LaFavoritaScrapper(url='http://www.lafavorita.com.uy/')
    for i in (a, b, c, d, e, f, g):
        i.scrap_dollar()
        print(i)
