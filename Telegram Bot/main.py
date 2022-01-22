import os
from replit import db
from telebot import telebot
from scraper import scrape
from keepalive import keep_alive
from util import watchlisted, is_number

key = os.environ.get('telegram_key')
bot = telebot.TeleBot(key, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    username = message.chat.first_name
    text = f"Hello {username} I’m <b>TrackrBot</b> &#129302;.\n\n<u><b>What I can do for you?</b></u>\n\n<b>&#8226; Send you Price Alerts</b>\nGet price alerts for your Amazon products. Just paste the product link in the chat to get started.\n\n<b>&#8226; Send you Price Charts</b>\nGet a graph of your product price every 30 days."
    bot.send_message(cid, text)

@bot.message_handler(commands=['help'])
def help(message):
    cid = message.chat.id
    text1 = "<u><b>Note</b></u>\n\n&#8226; To add a price alert for your Amazon product simply paste the product link in the chat.\n\n&#8226; You can add a maximum of 3 products to your watchlist.\n\n&#8226; Once you have reached the maximum limit on your watchlist you'll have to delete a product to add any more products.\n\n&#8226; If you like this project you can support it on <a href='https://www.buymeacoffee.com/rittik'>BuyMeACoffee.</a>"
    text2 = "<b>List of commands</b>\n\n<b>&#8226; /watchlist</b>\nTo see the products you have watchlisted\n\n<b>&#8226; /delete</b>\nTo delete products from your watchlist"

    bot.send_message(cid, text1, disable_web_page_preview=True)
    bot.send_message(cid, text2, disable_web_page_preview=True)


@bot.message_handler(commands=['watchlist'])
def watchlist(message):
    cid = message.chat.id
    key = str(cid)
    username = message.chat.first_name

    text1 = watchlisted(key,username)
    text2 = 'To delete a product from the watchlist use the /delete command.\n<b>Usage:</b> <code>/delete productNumber</code>\n<b>Example:</b> <code>/delete 2</code>'
    
    bot.send_message(cid, text1, disable_web_page_preview=True)
    bot.send_message(cid, text2, disable_web_page_preview=True)


@bot.message_handler(commands=['delete'])
def delete(message):
    cid = message.chat.id
    index = message.text.replace("/delete ", "") 

    if index == '/delete':
        text = '<b>Error:</b> productNumber is empty.\n<b>Usage:</b> <code>/delete productNumber</code>\n<i>(Check your /watchlist for productNumber)</i>'
    else:
        key = str(cid)
        db_len = len(db[key])
        username = message.chat.first_name

        if is_number(index):
            if int(index) <= db_len:
                index = int(index) - 1
                del db[key][index]
                text = watchlisted(key,username)
            else:
                text = '<b>Error:</b> productNumber out of range.'

        else:
            text = '<b>Error:</b> Please enter a valid number.'

    bot.send_message(cid, text, disable_web_page_preview=True)

restricted = os.environ.get('restrictedaccess')
@bot.message_handler(commands=[restricted])
def restrict(message):
    cid = message.chat.id
    key = str(cid)
    if key not in db['restricted']:
        db['restricted'].append(key)
        text = "You've been given restricted access."
        bot.send_message(cid, text)

@bot.message_handler(func=lambda message: True)
def main(message):
    cid = message.chat.id
    key = str(cid)
    timestamp_current = message.date
    timestamp_previous = db.get(key+'ts')
    
    if ((timestamp_previous == None) or (timestamp_current - timestamp_previous > 5)):
        db[key+'ts'] = timestamp_current

        if key in db.keys():
            if len(db[key]) >= 3:
                if key not in db['restricted']:
                    bot.send_message(cid, '<b>Error:</b> Your /watchlist is full!\nDelete a product from the watchlist to add a new product')
                    return 0

        if 'https://www.amazon.' in message.text:
            bot.send_message(cid,'Fetching data...')
            u1 = message.text.partition("https://www.amazon.")[1]
            u2 = message.text.partition("https://www.amazon.")[2]
            url = u1 + u2

            scraped = scrape(url) #scraping function

            if type(scraped) == tuple:
                data = {'title':scraped[1],'asin':scraped[2],'category':scraped[3],'uid':scraped[4],'url':url}
                
                if key in db.keys():
                    db[key].append(data)
                else:
                    db[key] = [data]
                bot.reply_to(message,f'<b>Product Name: </b><i>{scraped[1]}</i>\n\n<b>Price: </b><i>{scraped[0]}</i>')
                echo = bot.reply_to(message,'Set a Price Alert for your product or Enter <b>0</b> to cancel the request\n<b>Example:</b> <i>140.99</i>')
                bot.register_next_step_handler(message=echo, callback=get_alertprice)

            elif scraped == 'exhausted': #api calls exhausted
                username = message.chat.first_name
                bot.reply_to(message, f"<b>Error: </b><code>API calls exhausted</code>\n\nHey {username} due to high number of users using <b>TrackrBot</b> an API which is used to provide this service has been exhausted for the month.\nTo support this project and ensure it keeps running smoothly consider making a donation at https://www.buymeacoffee.com/rittik.")

            else:
                bot.reply_to(message,'<b>Error:</b> Could not fetch the data. Please try again.')
        else:
            bot.reply_to(message,'Hey %s paste a valid Amazon product link in the chat to get started or press /help :)'%(message.chat.first_name))


def get_alertprice(message):
    cid = message.chat.id
    key = str(cid)
    index = len(db[key]) - 1

    if is_number(message.text):
        if int(message.text) == 0:
            del db[key][index]
            bot.send_message(cid,"Request cancelled.")
        else:
            db[key][index]['alert'] = message.text
            bot.send_message(cid,"<b>Successfully added to /watchlist &#129309;</b>\nYou'll recieve a notfication when your product reaches the target price.")

    else:
        inline_msg = 'Please enter a numeric value for the price alert (without the currency symbol) or Enter <b>0</b> to cancel the request'
        echo = bot.reply_to(message, inline_msg)
        bot.register_next_step_handler(message=echo, callback=get_alertprice)







while True:
    keep_alive()
    bot.infinity_polling()
