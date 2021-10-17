import os
import telebot

def send_alert(msg,cid):
    key = os.environ.get('telegram_key')
    bot = telebot.TeleBot(key, parse_mode='HTML')
    bot.send_message(cid, msg)