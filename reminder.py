import telebot

bot = telebot.TeleBot('1407012334:AAHKokzZtFovlYJZkr5i8nHcdknkT0EzmW4')


def reminder(user_id: str, link: str, actual_price: str, desired_price: str) -> None:
    """
    :param user_id: User's id
    :param link: Game URL
    :param actual_price: Actual game price at store
    :param desired_price: User's desired price
    :return: None

    Send message to user when the desired price is lower than actual price.
    Run after scrapy spider finished crawling and parsed price is lower then users desired price.
    """
    bot.send_message(user_id, f'Цена ниже указанной!\n'
                              f'Игра - {link}\n'
                              f'Цена - {actual_price}\n'
                              f'Указанная тобой цена - {desired_price}')


bot.polling()
