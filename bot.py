import telebot
import requests

params = {
    'chat_id': '920986648',
    'text': '',
}

token = '5642905344:AAEKmD3m4s1WTdXvOz-LRZMLA6qW4k46sQY'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['справка'])
def getReference(message):
    try:
        nameStudent = message.text.split(' ', 1)[1].split(':')[0] 
        group = message.text.split(' ', 1)[1].split(':')[1] 
        reference = message.text.split(' ', 1)[1].split(':')[2]
        params['text'] = nameStudent + ' ' + group + ' ' + reference
        bot.send_message(message.from_user.id, 'Успех') 
        response = requests.get('https://api.telegram.org/bot'+token+'/sendMessage', params=params)
    except IndexError:
        print(type(message.from_user.id))
        bot.send_message(
            message.from_user.id, 'Форма для получения справки:\n/справка ФИО:Группа:Справка')
    finally:
        return 0


bot.polling(none_stop=True)