from bs4 import BeautifulSoup
import requests
import lxml
import re
import time

def scrape(url):
    HEADERS1 = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    HEADERS2 = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    HEADERS3 = ({"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36", 
                "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"})

    
    HEADERS = [HEADERS1, HEADERS2, HEADERS3]
    for HEADER in HEADERS:
        time.sleep(0.01)
        page = requests.get(url, headers=HEADER)
        soup = BeautifulSoup(page.content, 'lxml')

        result = []
        def get_price(pid):
            price_raw = soup.find(id=pid).get_text()
            if '-' in price_raw:
                price_raw = price_raw.split('-')[0]
            price_formatted = re.sub("[^0123456789\.,]","",price_raw)
            print(price_formatted)
            if price_formatted[-3] == ',':
                price = price_formatted.replace('.','').replace(',', '.')
            else:
                price = price_formatted.replace(',', '').strip()

            return float(price)
        
        try:
            result = get_price('priceblock_ourprice')
            return result
        except:
            try:
                result = get_price('priceblock_dealprice')
                return result
            except:
                pass
        
    return 'NA'
