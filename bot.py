import telebot
import re
import random
from translate import Translator

token = ''

bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def start(message):
    if message.text.find("Привет") != -1:
      bot.send_message(message.from_user.id, f"Привет, {message.chat.first_name}! Чем я могу тебе помочь?")
    elif  message.text == "Что ты умеешь?":
      bot.send_message(message.from_user.id, "Я умею решать простые пример, переводить слова на английский язык, а также могу посоветовать хорошую музыку, фильм или игру.")
    elif  message.text.find("Сколько будет") != -1:
      newMessage = re.split(' ', message.text, 2)
      ex = re.split(' ', newMessage[2].replace('?', ''))
      if newMessage[2].find('+') != -1:
        bot.send_message(message.from_user.id, f"{ex[0]} + {ex[2]} = {int(ex[0]) + int(ex[2])}")
      elif newMessage[2].find('-') != -1:
        bot.send_message(message.from_user.id, f"{ex[0]} - {ex[2]} = {int(ex[0]) - int(ex[2])}")
      elif newMessage[2].find('*') != -1:
        bot.send_message(message.from_user.id, f"{ex[0]} * {ex[2]} = {int(ex[0]) * int(ex[2])}")
      elif newMessage[2].find('/') != -1:
        bot.send_message(message.from_user.id, f"{ex[0]} / {ex[2]} = {int(ex[0]) / int(ex[2])}")
    elif  message.text.find("Как будет") != -1:
      newMessage = re.split(' ', message.text)
      translator = Translator(from_lang="russian", to_lang="english")
      bot.send_message(message.from_user.id, f"{newMessage[2].replace(newMessage[2][0], newMessage[2][0].upper())} - {translator.translate(newMessage[2].replace(newMessage[2][0], newMessage[2][0].upper()))}")
    elif  message.text.find("Посоветуй") != -1:
      newMessage = re.split(' ', message.text)
      if newMessage[2].find("фильм") != -1:
        filmList = ["\"Зеленая миля\" - 1999 года, 189 минут.\n\nПол Эджкомб — начальник блока смертников в тюрьме «Холодная гора», каждый из узников которого однажды проходит «зеленую милю» по пути к месту казни. Пол повидал много заключённых и надзирателей за время работы. Однако гигант Джон Коффи, обвинённый в страшном преступлении, стал одним из самых необычных обитателей блока.", 
        "\"Список Шиндлера\" - 1993 года, 195 минут.\n\nФильм рассказывает реальную историю загадочного Оскара Шиндлера, члена нацистской партии, преуспевающего фабриканта, спасшего во время Второй мировой войны почти 1200 евреев.",
        "\"Побег из Шоушенка\" - 1994 года, 142 минуты.\n\nБухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения.",
        "\"Форрест Гамп\" - 1994 года, 142 минуты.\n\nCидя на автобусной остановке, Форрест Гамп — не очень умный, но добрый и открытый парень — рассказывает случайным встречным историю своей необыкновенной жизни."]
        bot.send_message(message.from_user.id, f"{filmList[random.randint(0, 3)]}")
      elif newMessage[2].find("музыку") != -1:
        musicList = ["Dark Red — Steve Lacy", "Alien Blues — Vundabar", "Taj Mahal — Broncho", "Who's Ready for Tomorrow — RAT BOY, IBDY"]
        bot.send_message(message.from_user.id, f"{musicList[random.randint(0, 3)]}")
      elif newMessage[2].find("игру") != -1:
        gameList = ["Detroit: Become Human\n\nВ Detroit: Become Human в ваших руках окажутся судьбы как человечества, так и андроидов. Каждый сделанный вами выбор повлияет на исход игры, в которой реализован одним из самых замысловатых и разветвленных сюжетов из когда-либо созданных в игровой индустрии.",
        "Red Dead Redemption 2\n\nИгра RDR2, получившая более 175 наград и 250 высших оценок от игровых изданий, – это грандиозная история о судьбе бандита Артура Моргана и банды Ван дер Линде, бегущих от закона через всю Америку на заре современной эпохи.",
        "The Witcher 3: Wild Hunt\n\nКогда в Северных королевствах бушует война, вы заключаете величайший контракт своей жизни — отыскать Дитя предназначения, живое оружие, которое может изменить облик мира.",
        "Cyberpunk 2077\n\nCyberpunk 2077 — приключенческая ролевая игра с открытым миром, действие которой происходит в футуристическом мегаполисе Найт-Сити, где выше всего ценятся власть, роскошь и модификации тела."]
        bot.send_message(message.from_user.id, f"{gameList[random.randint(0, 3)]}")
    elif  message.text == "Спасибо за помощь!":
      bot.send_message(message.from_user.id, "Я всегда рада помочь.")
    elif  message.text.find("Пока") != -1:
      bot.send_message(message.from_user.id, f"Пока, {message.chat.first_name}. Буду ждать твоего возвращения!")
    else:
      bot.send_message(message.from_user.id, "Прости, но я тебя не понимаю.")
      bot.send_message(message.from_user.id, "Может быть ты хотел решить какой-нибудь простой пример или перевести слово на английский язык?")
      bot.send_message(message.from_user.id, "Если хочешь, то я также могу посоветовать какую-нибудь музыку, игру или фильм.")

bot.polling(none_stop=True)