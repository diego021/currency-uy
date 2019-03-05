#!/usr/bin/env python3
from scrappers import scrapper, javascript 

sites = [ scrapper.GalesScrapper(url='http://www.gales.com.uy/home/'),
          scrapper.VarlixScrapper(url='https://www.varlix.com.uy/'),
          scrapper.Cambio18Scrapper(url='https://www.cambio18.com/'),
          scrapper.AspenScrapper(url='http://www.aspen.com.uy/sitio/'),
          scrapper.MatrizScrapper(url='https://www.cambiomatriz.com.uy/'),
          scrapper.IberiaScrapper(url='http://www.cambioiberia.com/'),
          scrapper.LaFavoritaScrapper(url='http://www.lafavorita.com.uy/'),
          javascript.IndumexScrapper(url='https://www.indumex.com/') ]

for site in sites:
    site.scrap_dollar()
    print(site)

