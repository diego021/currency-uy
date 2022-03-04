#!/usr/bin/env python3
from scrappers import javascript, scrapper

# TODO: Move to settings file
persist_data = False

sites = [
    scrapper.GalesScrapper(url='http://www.gales.com.uy/home/'),
    scrapper.VarlixScrapper(url='https://www.varlix.com.uy/'),
    # scrapper.Cambio18Scrapper(url='https://www.cambio18.com/'),
    scrapper.AspenScrapper(url='http://www.aspen.com.uy/sitio/'),
    scrapper.MatrizScrapper(url='https://www.cambiomatriz.com.uy/'),
    # scrapper.IberiaScrapper(url='http://www.cambioiberia.com/'),
    scrapper.LaFavoritaScrapper(url='http://www.lafavorita.com.uy/'),
    # javascript.IndumexScrapper(url='https://www.indumex.com/')
]


for site in sites:
    print(javascript)  # Remove after module in use
    site.prepare()
    site.scrap_dollar()
    print(site)
