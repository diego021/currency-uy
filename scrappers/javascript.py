#!/usr/bin/env python3
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from .scrapper import ScrapperBase

class JavascriptScrapper(ScrapperBase):
    '''Superclass containing common things to dynamic scrappers'''

    def __init__(self, url):
        if sys.platform == 'linux':
            myphantomjs = 'scrappers/drivers/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
        elif sys.platform == 'darwin':
            myphantomjs = 'scrappers/drivers/phantomjs-2.1.1-macosx/bin/phantomjs'
        else:
            raise NotImplementedError('This OS is not currently supported')
        driver = webdriver.PhantomJS(executable_path=myphantomjs)
        driver.get(url)
        html = driver.page_source
        self.soup = BeautifulSoup(html, 'html.parser')
        self.name = ''
        self.rates = {}

class IndumexScrapper(JavascriptScrapper):
    '''Dynamic: javascript feeds rates divs'''

    def __init__(self, *args, **kwargs):
        JavascriptScrapper.__init__(self, *args, **kwargs)
        self.name = 'Cambio Indumex'
        self.rates_div = self.soup.find('div', attrs={'class': 'rates'}).find('div')

    def scrap_dollar(self):
        buy = self.rates_div.find('span', id='compraDolar').text # Empty
        sell = self.rates_div.find('span', id='ventaDolar').text # Empty
        self.rates.update({'dollar': {'buy': buy, 'sell': sell}})

if __name__ == '__main__':
    a = IndumexScrapper(url='https://www.indumex.com/')
    a.scrap_dollar()
    print(a)

