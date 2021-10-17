import os
import json
from replit import db
import gspread
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

def send_data(data):
    product_name = data[0][:20].strip().replace(' ', '') + '_' + str(data[3])
    data.insert(1, product_name)

    n = len(meta.col_values(1))
    for row,datae in zip(range(1,6),data):
        meta.update_cell(n+1, row, datae)

    price.update_cell(1, n, data[1])

def list_my_products(cid,name):
    while db['key'] == 1:
        if db['key'] == 0:
            break
    db['key'] = 1
    cell_list = meta.findall(cid)
    if len(cell_list) != 0:
        message = "Here's a list of your products %s\n\n"%(name)
        for i in range(0,len(cell_list)):
            row = cell_list[i].row
            col_val = meta.row_values(row)
            message += "<b>Product Name: </b><a href='%s'>%s</a>\n<b>Price Alert: </b>%s \n\n"%(col_val[3],col_val[0],col_val[2])
    else:
        message = "%s you haven't added any products to the watchlist yet."%(name)

    db['key'] = 0

    return message
