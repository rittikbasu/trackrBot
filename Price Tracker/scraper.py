from bs4 import BeautifulSoup
import requests
import lxml
import re
import os
from func_timeout import func_set_timeout

from helper import scraper_cc

def get_html(url):
    api_key = os.environ.get('scraperapi_key')
    cc = scraper_cc(url)
    @func_set_timeout(20)
    def runfastordie():
        page = requests.get(f'http://api.scraperapi.com?api_key={api_key}&url={url}country_code={cc}')
        soup = BeautifulSoup(page.content,'lxml')
        print(page)
        return soup
    
    for iter in range(0,3):
        print(iter)
        try:
            soup = runfastordie()
            p1 = soup.select_one('span.a-price.a-text-price.a-size-medium.apexPriceToPay')
            p2 = soup.select_one('.a-color-base .a-size-base')
            p3 = soup.find(id='outOfStock') 
            p4 = soup.find(id='newBuyBoxPrice') #us
            p5 = soup.select_one('.a-size-medium.a-color-price.header-price') #us
            p6 = soup.select_one('.aok-align-center > span > span.a-offscreen') #fr
            if p3 != None:
                p3 = 'outOfStock'
            values = [p1,p2,p3,p4,p5,p6]
            print(values)
            for value in values:
                if value != None:
                    return value
        except:
            continue
    return None


def process_price(price_raw):
    if '-' in price_raw:
        price_raw = price_raw.split('-')[0]
    price_formatted = re.sub("[^0123456789\.,]","",price_raw)
    try:
        if price_formatted[-3] == ',':
            price = price_formatted.replace('.','').replace(',', '.')
        else:
            price = price_formatted.replace(',', '').strip()
    except IndexError:
        return float(price_formatted)
    return float(price)

def scrape(url):
    price_html = get_html(url)
    if price_html == None:
        return 0

    try:
        price_raw = price_html.select_one('.a-offscreen').get_text()
        price = process_price(price_raw)

    except Exception as e:
        print(e)
        try:
            price_raw = price_html.get_text()
            price = process_price(price_raw)
        except:
            price = 0

    return price
