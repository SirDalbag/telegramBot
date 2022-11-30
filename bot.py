import telebot
import re
import random
from translate import Translator

token = ''

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def start(message):
    

bot.polling(none_stop=True)