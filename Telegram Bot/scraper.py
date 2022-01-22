from bs4 import BeautifulSoup
import requests
import lxml
import re
import os
import shortuuid
from func_timeout import func_set_timeout

def get_html(url):
    api_key = os.environ.get('scraperapi_key')
    @func_set_timeout(20)
    def runfastordie():
        page = requests.get('http://api.scraperapi.com?api_key='+api_key+'&url='+url)
        soup = BeautifulSoup(page.content,'lxml')
        print(page)
        if str(page) == '<Response [403]>':
            return 0
        return soup
    
    for iter in range(0,3):
        print(iter)
        try:
            soup = runfastordie()
            if soup == 0:
                return 0
            p1 = soup.select_one('span.a-price.a-text-price.a-size-medium.apexPriceToPay')
            p2 = soup.select_one('.a-color-base .a-size-base')
            p3 = soup.find(id='outOfStock') 
            p4 = soup.find(id='newBuyBoxPrice') #us
            p5 = soup.select_one('.a-size-medium.a-color-price.header-price') #us
            p6 = soup.select_one('.aok-align-center > span > span.a-offscreen') #fr
            values = [p1,p2,p3,p4,p5,p6]
            print(values)
            for value in values:
                if value != None:
                    return soup, value
        except:
            continue
    return None

def process_price(price_raw):
    if '-' in price_raw:
        price_raw = price_raw.split('-')[0]
    price_formatted = re.sub("[^0123456789\.,]","",price_raw)

    if price_formatted[-3] == ',':
        price = price_formatted.replace('.','').replace(',', '.')

    else:
        price = price_formatted.replace(',', '').strip()
    return price

def metadata(soup,url):
    try:
        search_asin = re.search('/(?:dp|o|gp/product|-)\/(B[0-9]{2}[0-9A-Z]{7}|[0-9]{9}(?:X|[0-9]))/', url)
        if search_asin != None:
            asin = search_asin.group(1)
        else:
            asin = soup.find(id='ASIN')['value']
        category = soup.find(id='dp')['class'][0]
        title = soup.find(id='productTitle').get_text().strip()
        uid = shortuuid.uuid()

        return title,asin,category,uid
    except Exception as e:
        print(e)
        return 'error'

def scrape(url):
    result = get_html(url)
    if result == None:
        return 'error'
    if result == 0:
        return 'exhausted'

    soup = result[0]
    price_html = result[1]

    try:
        price_raw = price_html.select_one('.a-offscreen').get_text()
        price = process_price(price_raw)

    except Exception as e:
        print(e)
        try:
            price_raw = price_html.get_text()
            if len(price_raw) > 10:
                raise Exception('Not a book') 
            price = process_price(price_raw)
        except:
            if price_html != None:
                price = 'Out of stock'
            else:
                price = 'error'
                return price

    meta = metadata(soup,url)
    if meta != 'error':
        return price, meta[0], meta[1], meta[2], meta[3]
    else:
        return 'error'
