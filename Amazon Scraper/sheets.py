import os
import json
import gspread
import datetime
from scrape import scrape
from telegram import send_alert
from oauth2client.service_account import ServiceAccountCredentials

key = os.environ.get('sheets_key')
key = json.loads(key)
scope = ['https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(key, scope)
client = gspread.authorize(creds)

sheet = client.open('amazonPriceAlert')
price = sheet.get_worksheet(1)
meta = sheet.get_worksheet(2)

def delete(indexes):
    for index in indexes:
        price.delete_columns(index)
        meta.delete_rows(index+1)

def write_data():
    meta_data = meta.get_all_values()
    n = len(meta_data)
    current_date = str(datetime.date.today())
    indexes = [] 

    for i in range(1,n):
        cid = meta_data[i][4]
        name = meta_data[i][1]
        alert = float(meta_data[i][2])
        url = meta_data[i][3]
        print(name,alert,cid,url)
        
        col_val = price.col_values(i)
        n = len(col_val)

        prev_date = col_val[-1][:10]
        try:
            prev_price = float(col_val[-1][11:])
        except:
            prev_price = 'NA'

        current_price = scrape(url)
        if current_price != 'NA' and current_price <= alert:
            msg = "<b>Alert</b>&#10071;&#10071;&#10071;\nYour product <a href='%s'><b>%s</b></a> is now available at <b>%d</b>"%(url,meta_data[i][0],current_price)
            send_alert(msg,cid)
            indexes.append(i)

        else:
            data = current_date + '_' + str(current_price)
            print(prev_price,current_price)
            if prev_date == current_date:
                if current_price == 'NA':
                    pass
                elif prev_price == 'NA' or prev_price > current_price:
                    price.update_cell(n, i, data)
            else:
                price.update_cell(n+1, i, data)
    delete(indexes)