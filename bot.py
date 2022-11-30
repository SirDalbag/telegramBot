# -*- coding: utf-8 -*-
import telebot
import re
import json

topics = {}

is_admin = 0

token = ''

bot = telebot.TeleBot(token)


def write(dict):
    dict_json = json.dumps(dict)
    with open("topics.json", "w") as file:
        file.write(dict_json)


def read(dict):
    with open("topics.json", "r") as file:
        dict_json = file.read()
    dict = json.loads(dict_json)


def add(key, val, dict):
    dict[key] = val
    write(dict)
    read(dict)


def remove(key, dict, all=0):
    if all == 1:
        dict.clear()
    else:
        del dict[key]
    write(dict)
    read(dict)


def edit(key, val, dict):
    dict[key] = val
    write(dict)
    read(dict)


@bot.message_handler(content_types=["text"])
def start(message):
    read(topics)
    if message.text.find("- это?") != -1:
        bot.send_message(
            message.from_user.id, f"{re.split(' ', message.text, 1)[0]}\n\n{topics.get(re.split(' ', message.text, 1)[0])}")
    elif message.text.find("Авторизация") != -1:
        if re.split(':', re.split(' ', message.text, 1)[1])[0] == "Admin" and re.split(':', re.split(' ', message.text, 1)[1])[1] == "Admin":
            global is_admin
            is_admin = 1
            bot.send_message(message.from_user.id,
                             "Права администратора получены.")
        else:
            bot.send_message(message.from_user.id,
                             "Права администратора не были получены.")
    elif message.text.find("Добавь") != -1:
        if is_admin == 1:
            add(re.split(':', re.split(' ', message.text, 1)[1])[0], re.split(
                ':', re.split(' ', message.text, 1)[1])[1], topics)
            bot.send_message(
                message.from_user.id, f"Тема \"{re.split(':', re.split(' ', message.text, 1)[1])[0]}\" успешно добавлена!")
        else:
            bot.send_message(message.from_user.id,
                             "Добавлять темы может только администратор.")
    elif message.text.find("Удали") != -1:
        if is_admin == 1:
            if message.text.find("все") != -1:
                remove(re.split(' ', message.text, 1)[1], topics, 1)
                bot.send_message(
                    message.from_user.id, "Все темы успешно удалены!")
            else:
                remove(re.split(' ', message.text, 1)[1], topics)
                bot.send_message(
                    message.from_user.id, f"Тема \"{re.split(' ', message.text, 1)[1]}\" успешно удалена!")
        else:
            bot.send_message(message.from_user.id,
                             "Удалять темы может только администратор.")
    elif message.text.find("Измени") != -1:
        if is_admin == 1:
            edit(re.split(':', re.split(' ', message.text, 1)[1])[0], re.split(
                ':', re.split(' ', message.text, 1)[1])[1], topics)
            bot.send_message(
                message.from_user.id, f"Тема \"{re.split(':', re.split(' ', message.text, 1)[1])[0]}\" успешно изменена!")
        else:
            bot.send_message(message.from_user.id,
                             "Изменять темы может только администратор.")
    elif message.text.find("Темы") != -1:
        for key in topics:
            bot.send_message(message.from_user.id,
                             f"{key}\n\n{topics[key]}")
    else:
        bot.send_message(message.from_user.id,
                         "Прости, но я тебя не понимаю.")


bot.polling(none_stop=True)
