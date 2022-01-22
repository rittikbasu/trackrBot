import os
from telebot import telebot

key = os.environ.get('telegram_key')
bot = telebot.TeleBot(key, parse_mode='HTML')

def send_alert(cid,product,price):
    url = product.get('url','None')
    title = product.get('title','None')
    message = f'<b>Alert</b>&#10071;&#10071;&#10071;\nYour product <a href="{url}"><b>{title}</b></a> is now available at <b>{price}</b>'
    bot.send_message(int(cid), message)

def send_graph(cid,image_path,product):
    title = product.get('title','None')
    message = f'<b>Price Chart:</b> <i>{title}</i>'
    bot.send_photo(int(cid), open(image_path, 'rb'), caption=message)
    
