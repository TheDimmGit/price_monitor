import telebot
import requests
import os
from db import db_saver, db_extract, db_delete, price_update, user_urls_extract, link_extract
bot = telebot.TeleBot('1407012334:AAHKokzZtFovlYJZkr5i8nHcdknkT0EzmW4')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard1.row('Добавить игру', 'Удалить игру', 'Показать список игр')


@bot.message_handler(commands=['start'])
def start_message(message):
    username = message.chat.first_name
    bot.send_message(message.chat.id, f'Привет, {username}!\n'
                                      f'Я Капитан Прайсер и я слежу за ценами! \n'
                                      f'Отправь мне ссылку на игру из Steam или GOG',
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
    elif message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Ну здравствуй')
    elif message.text.lower() == 'как дела?':
        bot.send_message(message.chat.id, 'У меня нет времени на разговоры, тыкай на мои кнопки!')
    else:
        bot.send_message(message.chat.id, 'Ты шо, чорт?!'
                                          '\nПользуйся кнопками, я шо, зря их тебе показываю?!', reply_markup=keyboard1)


def delete_game(message):
    user_id = message.chat.id
    if message.text in user_urls_extract(user_id):
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
        game_str += f'\n {i+1}. {j[0]} \n Желаемая цена - {j[1]} \n Актуальная цена на сайте - {j[2]}' \
                    f'\n___________________________________'
    return game_str.strip('\n')


def saver(message):
    if 'https://store.steampowered.com/app/' in message.text:
        if message.text in link_extract(message.chat.id):
            bot.send_message(message.chat.id, 'Такая игра уже есть', reply_markup=keyboard1)
        else:
            print(link_extract(message.chat.id))
            store = 'Steam'
            db_saver(message.chat.id, message.text, store)
            bot.send_message(message.chat.id, 'Игра из Steam добавлена', reply_markup=keyboard1)
            msg = bot.send_message(message.chat.id, 'Теперь скажи мне желаемую цену')
            bot.register_next_step_handler(msg, add_price)
    elif 'https://www.gog.com/game/' in message.text:
        if message.text in link_extract(message.chat.id):
            bot.send_message(message.chat.id, 'Такая игра уже есть', reply_markup=keyboard1)
        else:
            store = 'GOG'
            db_saver(message.chat.id, message.text, store)
            bot.send_message(message.chat.id, 'Игра из GOG добавлена \nЦены указаны в долларах', reply_markup=keyboard1)
            msg = bot.send_message(message.chat.id, 'Теперь скажи мне желаемую цену')
            bot.register_next_step_handler(msg, add_price)
    else:
        bot.send_message(message.chat.id, 'Я с такими ссылками не работаю, только Steam и GOG', reply_markup=keyboard1)


def add_price(message):
    user_id = message.chat.id
    if message.text.isdigit():
        text = 'Я сообщу, когда игра будет по указанной цене'
        price_update(message.text, user_id)
        bot.send_message(message.chat.id, text, reply_markup=keyboard1)
    else:
        text = 'Цена указана не корректно даваай еще раз'
        msg = bot.send_message(message.chat.id, text, reply_markup=keyboard1)
        bot.register_next_step_handler(msg, add_price)


# Running bot
bot.polling()
