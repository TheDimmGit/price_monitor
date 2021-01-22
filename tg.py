import telebot
import requests
from db import db_saver, db_extract, db_delete, price_set, user_urls_extract
from apscheduler.schedulers.blocking import BlockingScheduler
import os
bot = telebot.TeleBot('1407012334:AAHKokzZtFovlYJZkr5i8nHcdknkT0EzmW4')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard1.row('Добавить игру', 'Удалить игру', 'Показать список игр')


@bot.message_handler(commands=['start'])
def start_message(message) -> None:
    """
    :param message: User's input
    :return: None

     Greets user and shows main buttons 'Add game', 'Delete game' and 'Show all my games'.
    """
    username = message.chat.first_name
    bot.send_message(message.chat.id, f'Привет, {username}!\n'
                                      f'Я Капитан Прайсер и я слежу за ценами! \n'
                                      f'Отправь мне ссылку на игру из Steam или GOG',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message) -> None:
    """
    :param message: User's input
    :return: None

    Await for selected button.
    - 'Add game' - bot adds game to DB;
    - 'Delete game' - bot deletes game from DB;
    - 'Show all my games' - bot shows list of user's games.
    Warn user if input is incorrect.
    """
    user_id = message.chat.id
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


def delete_game(message) -> None:
    """
    :param message: User's input
    :return: None

    Check is URL exists in DB, if so, deletes specific URL from DB.
    """
    user_id = message.chat.id
    if message.text in user_urls_extract(user_id):
        db_delete(message.text, user_id)
        bot.send_message(message.chat.id, 'Игра успешно удалена', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Такой игры нет в списке', reply_markup=keyboard1)


def process_url_step(message) -> None:
    """
Check whether URL is responding and accurate, if so, save URL to DB,
if not, warn user.
    """
    try:
        resp = requests.get(message.text).status_code
        if resp == 200:
            saver(message)
        else:
            bot.send_message(message.chat.id, 'Эта ссылка не активна', reply_markup=keyboard1)
    except (requests.exceptions.MissingSchema, requests.exceptions.InvalidURL):
        bot.send_message(message.chat.id, 'Какая-то странная ссылка', reply_markup=keyboard1)


def url_list_generate(user_id: str) -> str:
    """
    :param user_id: User's id
    :return: list of user's games with desired and actual prices

Concatenate game number, desired and actual prices strings.
    """
    game_str = ''
    for i, j in enumerate(db_extract(user_id)):
        p = j[2]
        if j[2] == -1:
            p = 'Игра бесплатная'
        elif j[2] == 0:
            p = 'Подождите, цена уточняется...'
        game_str += f'\n {i+1}. {j[0]} \n Желаемая цена - {j[1]} \n Актуальная цена на сайте - {p}' \
                    f'\n___________________________________'
    return game_str.strip('\n')


def saver(message) -> None:
    """
   Check whether store is acceptable or not;
   Check if URL is already exists in DB, warn user if is, add URL if not;
   Ask user for desired price.

    """
    if 'https://store.steampowered.com/app/' in message.text:
        if message.text in user_urls_extract(message.chat.id):
            bot.send_message(message.chat.id, 'Такая игра уже есть', reply_markup=keyboard1)
        else:
            store = 'Steam'
            db_saver(message.chat.id, message.text, store)
            bot.send_message(message.chat.id, 'Игра из Steam добавлена', reply_markup=keyboard1)
            msg = bot.send_message(message.chat.id, 'Теперь скажи мне желаемую цену')
            bot.register_next_step_handler(msg, add_price)
    elif 'https://www.gog.com/game/' in message.text:
        if message.text in user_urls_extract(message.chat.id):
            bot.send_message(message.chat.id, 'Такая игра уже есть', reply_markup=keyboard1)
        else:
            store = 'GOG'
            db_saver(message.chat.id, message.text, store)
            bot.send_message(message.chat.id, 'Игра из GOG добавлена', reply_markup=keyboard1)
            msg = bot.send_message(message.chat.id, 'Теперь скажи мне желаемую цену')
            bot.register_next_step_handler(msg, add_price)
    else:
        bot.send_message(message.chat.id, 'Я с такими ссылками не работаю, только Steam и GOG', reply_markup=keyboard1)


def add_price(message) -> None:
    """
   Set desired price for specific game, warn user if price is not accurate.
    """
    user_id = message.chat.id
    if message.text.isdigit():
        text = 'Я сообщу, когда игра будет по указанной цене'
        price_set(message.text, user_id)
        bot.send_message(message.chat.id, text, reply_markup=keyboard1)
    else:
        text = 'Цена указана не корректно даваай еще раз'
        msg = bot.send_message(message.chat.id, text, reply_markup=keyboard1)
        bot.register_next_step_handler(msg, add_price)


sched = BlockingScheduler()


@sched.scheduled_job('interval', seconds=20)
def timed_job():
    os.system('scrapy crawl steam')


@sched.scheduled_job('interval', seconds=30)
def timed_job():
    os.system('scrapy crawl gog')


@sched.scheduled_job('interval', seconds=0)
def timed_job():
    bot.polling()


sched.start()
