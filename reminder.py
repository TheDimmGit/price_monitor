import telebot

bot = telebot.TeleBot('1407012334:AAHKokzZtFovlYJZkr5i8nHcdknkT0EzmW4')


def reminder(user_id, link, actual_price, desired_price):
    bot.send_message(user_id, f'Цена ниже указанной!\n'
                              f'Игра - {link}\n'
                              f'Цена - {actual_price}\n'
                              f'Указанная тобой цена - {desired_price}')


bot.polling()
