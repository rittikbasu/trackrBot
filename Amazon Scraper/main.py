import os
import time
import json
import gspread
import datetime
import schedule
from replit import db
from oauth2client.service_account import ServiceAccountCredentials

from scraper import scrape
from graph import plot_graph
from sendtotelegram import send_alert
from helper import next_available_col, next_available_row, get_country_code, string_to_list_and_back
from keepalive import keep_alive

# -----------------------------GSHEETS CREDENTIALS ----------------------------
key = os.environ.get('sheets_key')
db.db_url = os.environ.get('db_url')
key = json.loads(key)
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(key, scope)
client = gspread.authorize(creds)

# -------------------------GET VALUES FROM WORKSHEETS -------------------------
sheet = client.open('amazonPriceAlert')
pricesheet = sheet.get_worksheet(4)
datasheet = sheet.get_worksheet(3)

# -------DELETES PRODUCTS NOT THERE IN THE DB ANYMORE FROM PRICESHEET ---------
def delete():
    ps_row_val = pricesheet.row_values(1)
    uidlist = []
    for key in db.keys():
        try:
            for elem in db[key]:
                uid = elem.get('uid')
                if uid != None:
                    uidlist.append(uid)
        except TypeError:
            pass
        except Exception as e:
            print(e)
    for value in ps_row_val:
        if value not in uidlist:
            cell = pricesheet.find(value)
            pricesheet.delete_columns(cell.col)

# ------------------------UPDATE DATASHEET ----------------------------------
def update_datasheet(product,key):
    url = product.get('url')
    asin = product.get('asin')
    cc = get_country_code(url)
    asin_cc = asin + '_' + cc
    cid = key
    alert = product.get('alert')
    ds_cell = datasheet.find(asin_cc)
    if ds_cell == None:
        title = product.get('title')
        count = 1
        data = [[asin_cc,title,cid,count,alert,url]]
        row = next_available_row(datasheet)
        ds_range = 'A' + str(row) + ':' + 'F' + str(row)

    else:
        row = ds_cell.row
        cid_prev = datasheet.cell(row, 3).value
        result = string_to_list_and_back(cid_prev,cid)
        cid_new = result[0]
        increment = result[1]
        count = int(datasheet.cell(row, 4).value) + increment
        alerts_prev = datasheet.cell(row, 5).value
        alerts_new = string_to_list_and_back(alerts_prev,alert)[0]
        data = [[cid_new,count,alerts_new]]
        ds_range = 'C' + str(row) + ':' + 'E' + str(row)
    
    datasheet.update(ds_range, data)

# ------------------------UPDATE PRICESHEET ----------------------------------
def update_pricesheet(product,col,cid,index):
    alert = float(product.get('alert'))
    url = product.get('url')

    current_price = scrape(url)
    current_date = str(datetime.date.today())

    uid_col_val = pricesheet.col_values(col)
    row = len(uid_col_val) #number of rows in UID

    if row == 1: #when new products are added uid column is empty
        prev_date = None
        prev_price = None

    if row % 30 == 0: #every 30 days sends graph of price values
        plot_graph(uid_col_val[1:],cid,product)
    
    if row >= 2:
        last_val = uid_col_val.pop().split('_')
        prev_date = last_val[0]
        prev_price = float(last_val[1])

    data = current_date + '_' + str(current_price)

    if current_price != 0 and current_price <= alert:
        send_alert(cid,product,current_price)
        del db[cid][index]
        pricesheet.delete_columns(col)


    elif current_date == prev_date: 
        if (current_price != 0 and prev_price == 0) or ((current_price < prev_price) and current_price != 0):
            pricesheet.update_cell(row, col, data)

    else:
        pricesheet.update_cell(row+1, col, data)

# ----------------------------MAIN FUNCTION---------------------------------
def main():
    try:
        delete()
    except:
        time.sleep(300)
        delete()
    for key in db.keys():
        try:
            for index, product in enumerate(db[key]):
                alert = product.get('alert')
                if alert != None:
                    uid = product.get('uid')
                    print(uid)
                    uid_cell = pricesheet.find(uid)
                    if uid_cell == None:
                        col = next_available_col(pricesheet)
                        pricesheet.update_cell(1, col, uid)
                        update_datasheet(product,key)
                        uid_cell = pricesheet.find(uid)

                    update_pricesheet(product,uid_cell.col,key,index)
        except TypeError:
            pass
        except Exception as e:
            print(e)

#------------------------------END-----------------------------------------

schedule.every().day.at("00:00").do(main)

while True:
    keep_alive()
    time.sleep(3600)
    schedule.run_pending()
