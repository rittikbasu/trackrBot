import os
import time
from replit import db
from telebot import telebot, types
from keepalive import keep_alive
from sheets import send_data, list_my_products
from util import is_number
from scraper import scrape

key = os.environ.get('telegram_key')
bot = telebot.TeleBot(key, parse_mode='HTML')

def check_inline(cid):
    if len(db[cid][1]) != 0:
        for btns in db[cid][1]:
            bot.edit_message_reply_markup(btns[0], btns[1])
            db[cid][1].clear()

def get_message_data(echo,cid):
    inline_data = [echo.chat.id,echo.message_id]
    db[str_cid][1].append(inline_data)

@bot.message_handler(commands=['start'])
def start(message):
    cid = message.chat.id
    name = message.chat.first_name
    text = "Hello %s I’m <b>TARS the Price Alert Bot</b> &#129302;.\n\nHave you ever waited for the price of an Amazon product to drop and then miss it because you forgot to check it on this random day?\n\nDon’t worry cause I got your back now &#128074;. Just paste an Amazon product url in the chat and tell me the price at which I should send you an alert. I’ll be checking the site every hour so now you can rest assured that you’ll never miss when your favourite product goes on sale."%(name)
    bot.send_message(cid, text)

@bot.message_handler(commands=['help'])
def help(message):
    text = "<b>Let’s talk about what I can do for you</b>\n\n1. Paste any Amazon product url in the chat and then I’ll ask you for the price alert at which you want me to notify you. After successful completion of the steps, your product will be added to the watchlist.\n\n<b>Note:</b> While sharing the url for any wearable product make sure to select your size before you send the link to me, this way you’ll only get the price alert for your size of the product.\n\n2. /watchlist: Use this command to get a list of all your products that are on the watchlist."
    bot.reply_to(message, text)

@bot.message_handler(commands=['watchlist'])
def list_products(message):
    bot.send_chat_action(message.chat.id, 'typing')
    cid = str(message.chat.id)
    name = message.chat.first_name
    product_list = list_my_products(cid,name)
    bot.reply_to(message, product_list, disable_web_page_preview=True)

@bot.message_handler(func=lambda message: True)
def echo_msg(message):
    global cid, str_cid
    cid = message.chat.id
    str_cid = str(cid)
    db[str_cid] = [[],[]]
    check_inline(str_cid)
    bot.send_chat_action(message.chat.id, 'typing')
    if 'https://www.amazon.' in message.text:
        u1 = message.text.partition("https://www.amazon.")[1]
        u2 = message.text.partition("https://www.amazon.")[2]
        url = u1 + u2
        scraped = scrape(url)
        if len(scraped) != 0:
            db[str_cid][0].append(scraped[0])
            db[str_cid][0].append(url)
            echo = bot.reply_to(message,'Set a Price Alert for your product\n<b>Example:</b> 1400')
            bot.register_next_step_handler(message=echo, callback=extract_msg)
        else:
            bot.reply_to(message,'There is something wrong with the link, TARS could not extract the data. Please try again.')
    else:
        bot.reply_to(message,'Hey %s paste a valid Amazon product link in the chat to get started or press /help :)'%(message.chat.first_name))


def yes_no(message):
    check_inline(str_cid)
    keyboard = types.InlineKeyboardMarkup()
    yes_btn = types.InlineKeyboardButton(text='Yes', callback_data='yes')
    no_btn = types.InlineKeyboardButton(text='No', callback_data='no')
    keyboard.add(yes_btn,no_btn)
    inline_msg = '<b>Product Name: </b><a href="%s">%s</a>\n\n<b>Price Alert: </b>%s \n\nPress <b>Yes</b> to continue or <b>No</b> to discard and start again'%(db[str_cid][0][2],db[str_cid][0][0],db[str_cid][0][1])
    echo = bot.reply_to(message, inline_msg, reply_markup=keyboard, disable_web_page_preview=True)
    get_message_data(echo,str_cid)
    bot.register_next_step_handler(message=echo, callback=yes_no)
    

def extract_msg(message):
    check_inline(str_cid)
    if is_number(message.text):
        db[str_cid][0].insert(1,message.text)
        db[str_cid][0].append(cid)
        yes_no(message)

    if not is_number(message.text):
        keyboard = types.InlineKeyboardMarkup()
        cancel_btn = types.InlineKeyboardButton(text='Сancel', callback_data='cancel')
        keyboard.add(cancel_btn)
        inline_msg = 'Please enter a numeric value for the price alert (without the currency symbol) or press <b>Cancel</b> to exit.'
        echo = bot.reply_to(message, inline_msg, reply_markup=keyboard)
        get_message_data(echo,cid)
        bot.register_next_step_handler(message=echo, callback=extract_msg)


@bot.callback_query_handler(func=lambda call: True)
def callback(query):
    if query.data == 'yes':
        send_data(db[str_cid][0])
        bot.answer_callback_query(query.id,'Product added successfully to watchlist')
        bot.clear_step_handler_by_chat_id(cid)
        bot.edit_message_reply_markup(cid, query.message.message_id)
        bot.send_message(cid, "Product added successfully to the watchlist! &#127882; &#127882; &#127882;\nYou'll recieve a notfication when your product reaches the target price.")
        db[str_cid][1].clear()

    if query.data == 'no':
        bot.answer_callback_query(query.id,'Request Cancelled')
        bot.clear_step_handler_by_chat_id(cid)
        bot.edit_message_reply_markup(cid, query.message.message_id)
        db[str_cid][1].clear()
    if query.data == 'cancel':
        bot.answer_callback_query(query.id,'Request Cancelled')
        bot.clear_step_handler_by_chat_id(cid)
        bot.edit_message_reply_markup(cid, query.message.message_id)
        db[str_cid][1].clear()


while True:
    keep_alive()
    bot.infinity_polling()
