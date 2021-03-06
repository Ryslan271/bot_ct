from random import choice

import requests
from bs4 import BeautifulSoup as Bs
from models import db_session
from models.start import bot
from models.users import User, Game
from telebot import types

db_session.global_init('sqlite.db')


def answer_not(message):
    bot.send_message(message.chat.id, 'Я не знаю что даже ответить на' + ' <b><i>' + message.text + '</i></b> ' + '\n'
                                                                                                                  'Напиши мне вопрос и ответ для него, чтобы я мог научиться так же говорить как '
                                                                                                                  'и людишки\n'
                                                                                                                  'Напиши вот так:\n'
                                                                                                                  '\n'
                                                                                                                  '<b>/Обучить "Тут вопрос"="тут ответ на этот вопрос"</b>',
                     parse_mode='html'
                     )


def Error(message):
    sti = open('assets/hi2.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id,
                     "Ошибка, может вы ввели не правильную команду\n"
                     'Напиши вот так:\n'
                     '\n'
                     '<b>/Обучить (Тут вопрос)=(тут ответ на этот вопрос)</b>',
                     parse_mode='html'
                     )


def start_hct(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item2 = types.KeyboardButton("/Telegram")
    item3 = types.KeyboardButton("/vk")
    item1 = types.KeyboardButton("/help")

    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id,
                     " Чтобы начать общаться просто пиши и обучай этого бота :D",
                     reply_markup=markup
                     )


def game_dif(message):
    session = db_session.create_session()

    user_all = session.query(Game).all()
    game_all = []

    for all in user_all:
        game_all.append(all.game)

    print(game_all)

    n = choice(game_all)

    mar = types.InlineKeyboardMarkup()
    mar.add(types.InlineKeyboardButton('игра', url=n))
    try:
        for all in user_all:
            if all.game == n:
                msg = all.answer_game.split('|')
                print(msg)
                if len(msg) == 1:
                    bot.send_message(message.chat.id,
                                     "Поиграй в эту игру\n" + all.answer_game,
                                     reply_markup=mar
                                     )
                    break
                else:
                    bot.send_message(message.chat.id, choice(msg), reply_markup=mar)
                    break
            else:
                bot.send_message(message.chat.id,
                                 "Поиграй в эту игру и напиши сколько набрал  *результат (тут счет)",
                                 reply_markup=mar
                                 )
                break

    except RuntimeError:
        bot.send_message(message.chat.id, 'Ошибка')
        back(message)
        print('error/game_dif/1_try')


def weather_sup(message):
    try:
        f = False

        text = message.text.replace('/погода ', '')
        r = requests.get('https://sinoptik.ua/погода-' + text)

        html = Bs(r.content, 'html.parser')
        for all in html.select('#content'):

            bot.send_message(message.chat.id, 'погода на 7 дней:')

            for i in range(1, 8):
                v = '#bd' + str(i)
                for el in html.select(v):
                    day = el.select('.day-link')[0].text
                    date = el.select('.date')[0].text
                    month = el.select('.month')[0].text
                    t_min = el.select('.temperature .min')[0].text
                    t_max = el.select('.temperature .max')[0].text
                    bot.send_message(
                        message.chat.id,
                        " День недели : *" + str(day) + "*: \n   Дата : *" + str(
                            date) + "* \n   Месяц : *" + str(month) + "* \n   Мин. температура : *" + str(
                            t_min) + "* \n   Мах. температура : *" + str(t_max) + "* \n",
                        parse_mode="Markdown"
                    )

            for el in html.select('#content'):
                text = el.select('.description')[0].text

                bot.send_message(message.chat.id, 'Сегодняшний день:'
                                                  '\n' + text)
            f = True

        if not f:
            error_weather(message)

    except BaseException:
        print('error/weather_sup/1_try')
        error_weather(message)


def error_weather(message):

    text1 = message.text.replace('/погода ', '')


    bot.send_message(message.chat.id, 'Ошибка в системе\n'
                                      'Может нет такого города как' + ' ' + text1)

    bot.send_message(message.chat.id, 'Вводите вот так:\n'
                                      '\n'
                                      '/погода (ваш город)')
