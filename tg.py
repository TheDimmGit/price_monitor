import telebot
from db import db_saver, db_extract
bot = telebot.TeleBot('1407012334:AAHKokzZtFovlYJZkr5i8nHcdknkT0EzmW4')


@bot.message_handler(commands=['start', 'Start'])
def start_message(message):
    user_id = message.chat.id
    bot.send_message(message.chat.id, f'Привет, жмых, твой id -  {user_id}\n'
                                      f'Отправь мне ссылку на игру из Steam, GOG или Epic Store')


@bot.message_handler(content_types=['text'])
def send_text(message):
    user_id = message.chat.id
    print(user_id)
    if 'https://store.steampowered.com/app/' in message.text:
        bot.send_message(message.chat.id, 'Это стим')
        db_saver(message.chat.id, message.text)
    elif 'https://www.gog.com/game/' in message.text:
        bot.send_message(message.chat.id, 'Это GOG')
    elif 'https://www.epicgames.com/store/ru/product/' in message.text:
        bot.send_message(message.chat.id, 'Это эпик')
    elif message.text == '+':
        bot.send_message(message.chat.id, url_list_generate(user_id))
    else:
        bot.send_message(message.chat.id, 'Ты шо, чорт?!')


def url_list_generate(user_id):
    game_str = ''
    for i, j in enumerate(db_extract(user_id)):
        game_str += '\n' + str(i+1) + ". " + j
    return game_str.strip('\n')


bot.polling()
