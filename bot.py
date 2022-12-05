# -*- coding: utf-8 -*-
import json
import datetime
import telebot

token = '5837752378:AAFRN_VsN2hZIok2nGpoWkcZ67YeNEOSeTU'

bot = telebot.TeleBot(token)

schedule = {}

topics = {}

authorization = {}

with open('schedule.json', 'r', encoding='utf-8') as f:
    schedule = json.load(f)

with open('topics.json', 'r', encoding='utf-8') as f:
    topics = json.load(f)

with open('authorization.json', 'r', encoding='utf-8') as f:
    authorization = json.load(f)


def writeSchedule():
    with open('schedule.json', 'w', encoding="utf-8") as outfile:
        json.dump(schedule, outfile)


def writeTopics():
    with open('topics.json', 'w', encoding="utf-8") as outfile:
        json.dump(topics, outfile)


def writeAuthorization():
    with open('authorization.json', 'w', encoding="utf-8") as outfile:
        json.dump(authorization, outfile)


def get_day(day_name):
    return schedule.get(day_name, 'Расписание не найдено')


def get_item(day_name, item_name):
    return schedule.get(day_name).get(item_name, 'Предмет не найден')


def get_topic(topic_name):
    return topics.get(topic_name, 'Тема не найдена')


def get_user(user_name):
    return topics.get(user_name, 'Пользователь не найден')


def get_date(day_name, item_name):
    str = schedule.get(day_name).get(item_name, 'Предмет не найден')
    if str != 'Предмет не найден':
        date = str.split(' ')[2].replace('-', '.').split('.')
        dateF = datetime.date(int(date[5])+2000, int(date[4]), int(date[3]))
        return dateF
    else:
        return 'Предмет не найден'


def get_time(day_name, item_name):
    str = schedule.get(day_name).get(item_name, 'Предмет не найден')
    now = datetime.date.today()
    if str != 'Предмет не найден':
        date = str.split(' ')[2].replace('-', '.').split('.')
        dateF = datetime.date(int(date[5])+2000, int(date[4]), int(date[3]))
        return dateF - now
    else:
        return 'Предмет не найден'


def autorizationUser(user_name, pwd):
    if pwd == 'adminpwd':
        authorization[user_name] = '1'
    else:
        authorization[user_name] = '0'
    writeAuthorization()


def add_edit_item(day_name, item_name, val):
    item = schedule.get(day_name)
    item[item_name] = val
    writeSchedule()


def del_item(day_name, item_name):
    item = schedule.get(day_name).get(item_name, 'Предмет не найден')
    if item != 'Предмет не найден':
        schedule.get(day_name).pop(item_name)
        writeSchedule()
        return 'Предмет успешно удален'
    else:
        return 'Предмет не найден'


def add_edit_topic(topic_name, val):
    topics[topic_name] = val
    writeTopics()


def del_topic(topic_name):
    if topic_name in topics:
        topics.pop(topic_name)
        writeTopics()
        return 'Тема успешно удалена'
    else:
        return 'Тема не найдена'


@bot.message_handler(commands=['авторизация'])
def isAuthorization(message):
    user_id = str(message.from_user.id)
    user_pwd = message.text.split(' ')[1]
    autorizationUser(user_id, user_pwd)
    if authorization[user_id] == 1:
        bot.send_message(message.chat.id, 'Права администратора')
    else:
        bot.send_message(message.chat.id, 'Права пользователя')


@bot.message_handler(commands=['тема'])
def showTopic(message):
    try:
        if get_topic(message.text.split(' ')[1]) != 'Тема не найдена':
            topic = message.text.split(' ')[1]
            bot.send_message(message.from_user.id,f'{topic}\n\n{topics[topic]}')
        else:
            bot.send_message(message.from_user.id, 'Тема не найдена')
    except IndexError:
        for topic in topics:
            bot.send_message(message.from_user.id,f'{topic}\n\n{topics[topic]}')
    finally:
        return 0


@bot.message_handler(commands=['предмет'])
def showItem(message):
    for key, value in schedule.items():
        temp = list(schedule[key].items())
        for i in temp:
            if i[0] == message.text.split(' ')[1]:
                day = int(str(get_time(key, message.text.split(' ')[1])).split(',')[0].replace('days', ''))
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
            scheduleDay = list(schedule[message.text.split(' ')[1]].items())
            if message.text.split(' ', 2)[2] != 'сортировка':
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
        for key, value in schedule.items():
            items = list(schedule[key].items())
            bot.send_message(message.chat.id, f'[{key}]')
            for item in items:
                bot.send_message(message.chat.id, f'{item[0]} - {item[1]}')
            bot.send_message(message.chat.id, '----------------------')
    finally:
        return 0


@bot.message_handler(commands=['добавитьР'])
def addSchedule(message):
    user_id = str(message.from_user.id)
    if authorization[user_id] == '1':
        day = message.text.split(' ', 2)[1]
        item = message.text.split(' ', 2)[2].split(':', 1)[0]
        valueItem = message.text.split(' ', 1)[1].split(':', 1)[1]
        add_edit_item(day, item, valueItem)
        bot.send_message(message.chat.id, 'Расписание успешно изменено')
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав')


@bot.message_handler(commands=['удалитьР'])
def removeSchedule(message):
    user_id = str(message.from_user.id)
    if authorization[user_id] == '1':
        day = message.text.split(' ', 2)[1]
        item = message.text.split(' ', 2)[2]
        temp = del_item(day, item)
        if temp != 'Предмет не найден':
            bot.send_message(message.chat.id, 'Расписание успешно изменено')
        else:
            bot.send_message(message.chat.id, 'Предмет не найден')
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав')


@bot.message_handler(commands=['изменитьР'])
def editSchedule(message):
    user_id = str(message.from_user.id)
    if authorization[user_id] == '1':
        day = message.text.split(' ', 2)[1]
        item = message.text.split(' ', 2)[2].split(':', 1)[0]
        valueItem = message.text.split(' ', 1)[1].split(':', 1)[1]
        add_edit_item(day, item, valueItem)
        bot.send_message(message.chat.id, 'Расписание успешно изменено')
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав')


@bot.message_handler(commands=['добавитьТ'])
def addSchedule(message):
    user_id = str(message.from_user.id)
    if authorization[user_id] == '1':
        topic = message.text.split(' ', 1)[1].split(':', 1)[0]
        val = message.text.split(':', 1)[1]
        add_edit_topic(topic, val)
        bot.send_message(message.chat.id, 'Тема успешно добавлена')
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав')


@bot.message_handler(commands=['удалитьТ'])
def removeSchedule(message):
    user_id = str(message.from_user.id)
    if authorization[user_id] == '1':
        topic = message.text.split(' ', 1)[1]
        temp = del_topic(topic)
        if temp != 'Тема не найдена':
            bot.send_message(message.chat.id, 'Тема успешно удалена')
        else:
            bot.send_message(message.chat.id, 'Тема не найдена')
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав')


@bot.message_handler(commands=['изменитьТ'])
def editSchedule(message):
    user_id = str(message.from_user.id)
    if authorization[user_id] == '1':
        topic = message.text.split(' ', 1)[1].split(':', 1)[0]
        val = message.text.split(':', 1)[1]
        add_edit_topic(topic, val)
        bot.send_message(message.chat.id, 'Тема успешно изменена')
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав')


bot.polling(none_stop=True)
