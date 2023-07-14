import os
from dotenv import load_dotenv

import asyncio
import contextlib
import logging
from typing import NoReturn
import telebot
import datetime
import json
import traceback
from monitor import send_telegram



def get_bot_key():
    load_dotenv(dotenv_path='./.env')
    BOT_KEY = os.getenv('TOKEN')
    return BOT_KEY

bot = telebot.TeleBot(get_bot_key())

@bot.message_handler(commands=['start'])
def start_command(message):
   bot.send_message(
       message.chat.id,
       'Greetings! Send /servers for monitor server\'s statistics\n' +
       'To get help press /help.'
   )

@bot.message_handler(commands=['help'])
def help_command(message):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.add(
       telebot.types.InlineKeyboardButton(
           'Message the developer', url='telegram.me/amnrahwork'
       )
   )
   bot.send_message(
       message.chat.id,'Send /servers for monitor server\'s statistics',
       reply_markup=keyboard
   )

@bot.message_handler(commands=['servers'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('local server', callback_data='get-test-server')
    )
    
    bot.send_message(message.chat.id, 'Click on the server name:', reply_markup=keyboard)
    
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
   data = query.data
   if data.startswith('get-'):
       get_srv_callback(query)

def get_srv_callback(query):
   bot.answer_callback_query(query.id)
   send_exchange_result(query.message, query.data[4:])

def send_exchange_result(message, ex_code):
   bot.send_chat_action(message.chat.id, 'typing')
   data = json.loads(str(send_telegram()))
   bot.send_message(
       message.chat.id, serialize(data),
       parse_mode='HTML'
   )

def serialize(data):
   result = '<b>' + json.dumps(data['hostname']) + ':</b>\n\n' + \
            'OS: ' + json.dumps(data['system']['os']) + '\n' + \
            'Uptime: ' + json.dumps(data['uptime']) + '\n' + \
            'Time: ' + json.dumps(data['timestamp']) + '\n' + \
            'Cpu_count: ' + json.dumps(data['cpu_count']) + '\n' + \
            'Cpu_usage: ' + json.dumps(data['cpu_usage']) + '\n' + \
            'Memory_total: {:.2f} GB\n'.format(data['memory_total']) + \
            'Memory_used: {:.2f} GB\n'.format(data['memory_used']) + \
            'Memory_used_percent: ' + json.dumps(data['memory_used_percent']) + '%\n' + \
            'Storage_total: {:.2f} GB\n'.format(data['storage_total']) + \
            'Storage_used:  {:.2f} GB\n'.format(data['storage_used'])+ \
            'Storage_used_percent: ' + json.dumps(data['storage_used_percent']) + '%\n' + \
            '-------------------------' 
   return result

def delete_msg(chat_id,msg_id):
    bot.delete_message(chat_id, msg_id)

if __name__ == '__main__':
    bot.polling(none_stop=True)
