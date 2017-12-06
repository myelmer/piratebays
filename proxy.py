from bs4 import BeautifulSoup as bs
from urllib import request as req

# MAIN SETTINGS
URL_LIST = []
site = 'https://thepiratebay-proxylist.org/'

def getProxy ():
    # PROXYLIST IS BLOCKING BOTS SO IN ORDER TO GET DATA YOU HAVE TO IMPLEMENT THIS
    prox1 = req.Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    source = req.urlopen(prox1).read()
    soup = bs(source, 'html.parser')
    main_item = soup.find_all('tr', {'data-probe': True, 'data-domain': True})

    # LOOPING FOR EACH ITEM
    for item in main_item:
        # URL
        urlsoup = item.find('td', {'title': 'URL'})
        site_url = urlsoup.find('a')
        URL_LIST.append(site_url['href'])

    return URL_LIST

