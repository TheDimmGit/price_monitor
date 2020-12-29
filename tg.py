import telebot
import requests
from db import db_saver, db_extract, db_delete
bot = telebot.TeleBot('1407012334:AAHKokzZtFovlYJZkr5i8nHcdknkT0EzmW4')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard1.row('Добавить игру', 'Удалить игру', 'Показать список игр')


@bot.message_handler(commands=['start'])
def start_message(message):
    username = message.chat.first_name
    bot.send_message(message.chat.id, f'Привет, {username}!\n'
                                      f'Отправь мне ссылку на игру из Steam, GOG или Epic Store',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    user_id = message.chat.id
    print(user_id)
    if message.text.lower() == 'добавить игру':
        msg = bot.send_message(message.chat.id, 'Жду ссылку на игру')
        bot.register_next_step_handler(msg, process_url_step)
    elif message.text.lower() == 'показать список игр':
        if url_list_generate(user_id):
            bot.send_message(message.chat.id, url_list_generate(user_id), reply_markup=keyboard1)
        else:
            bot.send_message(message.chat.id, 'Список игр пуст', reply_markup=keyboard1)
    elif message.text.lower() == 'удалить игру':
        msg = bot.send_message(message.chat.id, 'Жду ссылку на игру для удаления')
        bot.register_next_step_handler(msg, delete_game)
    else:
        bot.send_message(message.chat.id, 'Ты шо, чорт?!', reply_markup=keyboard1)


def delete_game(message):
    user_id = message.chat.id
    if message.text in db_extract(user_id):
        db_delete(message.text)
        bot.send_message(message.chat.id, 'Игра успешно удалена', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Такой игры нет в списке', reply_markup=keyboard1)


def process_url_step(message):
    try:
        resp = requests.get(message.text).status_code
        print(resp)
        if resp == 200:
            saver(message)
        else:
            bot.send_message(message.chat.id, 'Эта ссылка не активна', reply_markup=keyboard1)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        bot.send_message(message.chat.id, 'Какая-то странная ссылка', reply_markup=keyboard1)


def url_list_generate(user_id):
    game_str = ''
    for i, j in enumerate(db_extract(user_id)):
        game_str += '\n' + str(i+1) + ". " + j
    return game_str.strip('\n')


def saver(message):
    if 'https://store.steampowered.com/app/' in message.text:
        if message.text in db_extract(message.chat.id):
            bot.send_message(message.chat.id, 'Такая игра уже есть', reply_markup=keyboard1)
        else:
            db_saver(message.chat.id, message.text)
            bot.send_message(message.chat.id, 'Игра из Steam добавлена', reply_markup=keyboard1)
    elif 'https://www.gog.com/game/' in message.text:
        bot.send_message(message.chat.id, 'Игра из GOG добавлена', reply_markup=keyboard1)
    elif 'https://www.epicgames.com/store/ru/product/' in message.text:
        bot.send_message(message.chat.id, 'Игра из Epic добавлена', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Ты шо, чорт?!', reply_markup=keyboard1)


bot.polling()
