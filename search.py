from bs4 import BeautifulSoup as bs
from urllib import request as req
import proxy

# GETTING PORXYIES
PROXY_URL = proxy.getProxy()

# VARIABLES
main_array = []          # ALL ITEM ARRAYS ARE IN  HERE AS A TUPLE
cathegory_array = []     # ITEM CATHEGORIES ARE IN HERE
stats_array = []         # ITEM STATUS (SEEDERS AND LEECHERS) WILL BE HERE
item_link_array = []     # ITEM LINKS ARE HERE
item_name_array = []     # ITEM NAMES ARE HERE
item_date_array = []     # ITEM UPLOADED DATES ARE HERE
item_size_array = []     # ITEM SIZES ARE HERE

def search_item(search_request):
    # MAIN SETTINGS
    search_term = search_request
    search_term.replace(' ', '_')
    site_link = ''

    # GETTING A CONECTION TO PROXY
    while True:

        for i in PROXY_URL:
            link = '{}/s/?q={}&category=0&page=0&orderby=99'.format(i, search_term)
            site_link = i

            try:
                source = req.urlopen(link).read()
                soup = bs(source, 'html.parser')
                main_item = soup.find_all('tr')
                result_count = soup.find('h2')
                if main_item != None:
                    break
            except Exception:
                continue
        break

    return site_link, result_count, main_item

'''RETURING VALUES SO CAN USE THEM LATER'''

def findCathegories(catItem):
    cath = ''
    cathegory_item = catItem.find('td', {'class': 'vertTh'})

    if cathegory_item != None:
        cathegory_item = str(cathegory_item).replace('(', '').replace(')', '')
        cSoup = bs(cathegory_item, 'html.parser')
        cItem = cSoup.find_all('a')

        # APPEND ON ARRAY
        for a in cItem:
            cath = cath + a.string + ' '
        cathegory_array.append(cath)

def findItemDetails(iItem, rlink):
    item_details_name = iItem.find('div', {'class': 'detName'})

    # ITEM NAME DETALS
    if item_details_name != None:
        main_item_details = item_details_name.find('a')

        # ITEM DETAIL NAME AND LINK
        item_name = main_item_details['title']
        item_name = item_name.replace('Details for ', '')
        item_link = main_item_details['href']
        item_link = str(rlink) + item_link

        # APPEND ON ARRAYS
        item_name_array.append(item_name)
        item_link_array.append(item_link)

    # ITEM DESCRIPTION DETAILS
    item_description_details = iItem.find('font', {'class': 'detDesc'})
    item_description_details = str(item_description_details).split('"detDesc">')[-1].split(', ULed by ')[0]

    # ITEM DATE AND SIZE
    if item_description_details != None:

        # DATE
        upload_date = item_description_details.split('Uploaded ')[-1].split(',')[0].replace(' ',' ')  # BTW THIS IS VERY TRICKY PART THE ASCII CODES
        for char in upload_date:                                                                      # ARE DIFFERENT BE CAREFULL TRY NOT TO TOUCH IT
            if char == ':':
                upload_date = upload_date.split(' ')[0]
                upload_date = upload_date + ' 2017'
        upload_date = upload_date.replace('-', '/').replace(' ', '/')

        # SIZE
        item_size = item_description_details.split('Size ')[-1].split(',')[0].replace(' ',' ').replace('MiB', 'MB').replace('GiB', 'GB')

        # APPENDING ARRAYS
        item_date_array.append(upload_date)
        item_size_array.append(item_size)

def findItemStats(sItem):
    final = ''
    a = 1
    stats = sItem.find_all('td', {'align': 'right'})
    for stats_item in stats:

        if a%2 == 0:
            final = final + stats_item.string
            a = 0

        elif a%2 != 0:
            final = final + stats_item.string + ' '
            a += 1

    stats_array.append(final)

def search_final(search):
    search_item(search)
    rlink, rcount, ritem = search_item(search)

    # SPLITTING RESULT COUNT
    result_count = str(rcount).split('(')[1].replace(')', '').replace('</h2>', '').replace('approx ', '').replace(' found', ' results found!')

    print(result_count)
    for item in ritem:
        findCathegories(item)
        findItemDetails(item, ritem)
        findItemStats(item)
    print('Done!')

    for i in range(len(item_name_array)):
        main_array.append((cathegory_array[i], item_date_array[i], item_name_array[i], item_size_array[i],
                           stats_array[i], item_link_array[i]))

    for p in main_array: print(p)
