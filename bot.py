# -*- coding: utf-8 -*-
import json
import datetime
import telebot

token = ''

bot = telebot.TeleBot(token)

data = {}

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def write():
    with open('data.json', 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile)


def get_day(day_name):
    return data.get(day_name, 'Расписание не найдено')


def get_items(day_name, item_name):
    return data.get(day_name).get(item_name, 'Предмет не найден')


def get_date(day_name, item_name):
    str = data.get(day_name).get(item_name, 'Предмет не найден')
    if str != 'Предмет не найден':
        date = str.split(' ')[2].replace('-', '.').split('.')
        dateF = datetime.date(int(date[5])+2000, int(date[4]), int(date[3]))
        return dateF
    else:
        return 'Предмет не найден'


def get_time(day_name, item_name):
    str = data.get(day_name).get(item_name, 'Предмет не найден')
    now = datetime.date.today()
    if str != 'Предмет не найден':
        date = str.split(' ')[2].replace('-', '.').split('.')
        dateF = datetime.date(int(date[5])+2000, int(date[4]), int(date[3]))
        return dateF - now
    else:
        return 'Предмет не найден'


def add_edit_item(day_name, item_name, val):
    item = data.get(day_name)
    item[item_name] = val
    write()


def del_item(day_name, item_name):
    item = data.get(day_name).get(item_name, 'Предмет не найден')
    if item != 'Предмет не найден':
        data.get(day_name).pop(item_name)
        write()
        return 'Предмет успешно удален'
    else:
        return 'Предмет не найден'


@bot.message_handler(commands=['предмет'])
def showItem(message):
    for key, value in data.items():
        temp = list(data[key].items())
        for i in temp:
            if i[0] == message.text.split(' ')[1]:
                day = int(str(get_time(key, message.text.split(' ')[1])).split(
                    ',')[0].replace('days', ''))
                if day > 0:
                    bot.send_message(message.chat.id, f'Осталось дней: {day}')
                    break
                else:
                    bot.send_message(message.chat.id, 'Предмет закончился')


@bot.message_handler(commands=['расписание'])
def showSchedule(message):
    try:
        scheduleDay = get_day(message.text.split(' ')[1])
        if scheduleDay != 'Расписание не найдено':
            scheduleDay = list(data[message.text.split(' ')[1]].items())
            if message.text.split(' ')[2] != 'сортировка':
                for items in scheduleDay:
                    bot.send_message(
                        message.chat.id, f'{items[0]} - {items[1]}')
            else:
                for items in scheduleDay:
                    if get_date(message.text.split(' ')[1], items[0]) > datetime.date.today():
                        bot.send_message(
                            message.chat.id, f'{items[0]} - {items[1]}')
        else:
            bot.send_message(message.chat.id, scheduleDay)
    except IndexError:
        for key, value in data.items():
            items = list(data[key].items())
            bot.send_message(message.chat.id, f'[{key}]')
            for item in items:
                bot.send_message(message.chat.id, f'{item[0]} - {item[1]}')
            bot.send_message(message.chat.id, '----------------------')
    finally:
        return 0


@bot.message_handler(commands=['добавить'])
def addSchedule(message):
    day = message.text.split(' ')[1]
    item = message.text.split(' ', 2)[2].split(':', 1)[0]
    valueItem = message.text.split(' ', 1)[1].split(':', 1)[1]
    add_edit_item(day, item, valueItem)
    bot.send_message(message.chat.id, 'Расписание успешно изменено')


@bot.message_handler(commands=['удалить'])
def removeSchedule(message):
    day = message.text.split(' ')[1]
    item = message.text.split(' ')[2]
    del_item(day, item)
    bot.send_message(message.chat.id, 'Расписание успешно изменено')


@bot.message_handler(commands=['изменить'])
def editSchedule(message):
    day = message.text.split(' ')[1]
    item = message.text.split(' ', 2)[2].split(':', 1)[0]
    valueItem = message.text.split(' ', 1)[1].split(':', 1)[1]
    add_edit_item(day, item, valueItem)
    bot.send_message(message.chat.id, 'Расписание успешно изменено')


bot.polling(none_stop=True)
