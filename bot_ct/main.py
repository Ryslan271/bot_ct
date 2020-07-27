from models.start import bot, mat, snac
from telebot import types
from models.support import answer_not, Error, start_hct, game_dif, weather_sup, error_weather
from models import db_session
from models.users import User, Questions
from random import choice

db_session.global_init('sqlite.db')


@bot.message_handler(commands=['start'])
def welcome(message):
    # стартовая функция
    sti = open('assets/hi.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item4 = types.KeyboardButton("/Начать_общение")
    item2 = types.KeyboardButton("/Telegram")
    item3 = types.KeyboardButton("/vk")
    item1 = types.KeyboardButton("/help")

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный для "
                     "для обучения и ты можешь его научить новым ответам на твои слова :D\n"
                     "<b>Прошу без мата</b>".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['vk'])
def vk(message):
    sti = open('assets/1.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    mar = types.InlineKeyboardMarkup()
    mar.add(types.InlineKeyboardButton('Мой вк', url='https://vk.com/id131836293'))
    bot.send_message(message.chat.id,
                     'Вот мой вк для связи со мной',
                     parse_mode='html',
                     reply_markup=mar)


@bot.message_handler(commands=['Telegram'])
def telegram(message):
    sti = open('assets/2.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    mar = types.InlineKeyboardMarkup()
    mar.add(types.InlineKeyboardButton('Моя телега', url='https://t.me/Dog_Python'))

    bot.send_message(message.chat.id,
                     'Вот моя телега для связи со мной',
                     parse_mode='html',
                     reply_markup=mar)


@bot.message_handler(commands=['help'])
def help(message):
    sti = open('assets/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item2 = types.KeyboardButton("/Telegram")
    item3 = types.KeyboardButton("/vk")
    item1 = types.KeyboardButton("/help")

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id,
                     'Я мини бот созданный для обучения\n'
                     'Просто пиши мне и если нет ответа то научи меня отвечать на твой вопроc\n'
                     '\n'
                     '<i><b>/Обучить (тут твой вопрос)=(тут ответ на вопрос)</b></i>',
                     parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(commands=['погода', 'Погода'])
def weather(message):
    try:
        text1 = message.text.split()
        r = ['/погода']

        for word in r:
            if word in text1:
                text1.remove(word)

        if text1:
            weather_sup(message)

        elif not text1:
            bot.send_message(message.chat.id, 'Вводите вот так:\n'
                                              '\n'
                                              '/погода (ваш город)')
    except BaseException:
        print('error/weather/1_try')
        error_weather(message)


@bot.message_handler(commands=['Начать_общение'])
def start_ht_com(message):
    start_hct(message)


@bot.message_handler(commands=['Играть', 'играть'])
def game_com(message):
    game_dif(message)


@bot.message_handler(commands=['bd'])
def db(message):
    try:
        session = db_session.create_session()

        iduser = message.from_user.id

        user_all = session.query(User).all()

        for all in user_all:
            if iduser == 943101770 or iduser == 1218845111:
                bot.send_message(message.chat.id,
                                 "Слово: " + str(all.question) + '\n' + " Ответ: " + str(all.answer))
            else:
                bot.send_message(message.chat.id,
                                 'Вы не имеете доступ к этой команде')

    except BaseException:
        print('error/db/1_try')
        bot.send_message(message.chat.id,
                         'Ошибка, на входе в базу данных')


@bot.message_handler(commands=['Обучить', 'обучить'])
def training(message):
    message.text = message.text.replace('/Обучить ', '')

    try:
        msg = message.text.split('=')

        answer = msg[1].lower()
        question = msg[0].lower().lstrip()

        session = db_session.create_session()

        user_all = session.query(User).all()

        f = True

        for all in user_all:
            try:
                if f:
                    for i in mat:
                        for j in snac:
                            if j in answer.split() or j in question.split():
                                answer = answer.replace(j, '')
                                question = question.replace(j, '')

                            if i in answer.split() or i in question.split():
                                bot.send_message(message.chat.id, 'Пиши без мата, друг )')
                                f = False
                                break
                    if f:
                        if session.query(User).filter(User.question == question).first():
                            if session.query(User).filter(User.answer != answer).first():
                                if all.question == question:
                                    all.answer += '|' + answer
                                    session.commit()
                                    break
                            else:
                                bot.send_message(message.chat.id, 'Такой ответ уже есть на' + all.question + ' этот вопрос')
                                break
                        else:
                            user = User(
                                question=question,
                                answer=answer,
                            )
                            session.add(user)
                            session.commit()
                            break

            except RuntimeError:
                bot.send_message(message.chat.id, 'Ошибка')
                print('error/training/2_try')

    except BaseException:
        Error(message)
        print('error/training/1_try')


@bot.message_handler(content_types=['text'])
def text(message):
    if message.chat.type == 'private':
        session = db_session.create_session()

        user_all = session.query(User).all()
        user_wt = session.query(Questions).all()

        try:
            for all in user_all:
                try:

                    if '*результат' in message.text:
                        message.text = message.text.replace('*результат', '')

                        if int(message.text) > 100:

                            bot.send_message(message.chat.id, 'а ты молодец однако')
                            msg = []
                            for wt in user_wt:
                                msg.append(wt.question)
                            bot.send_message(message.chat.id, choice(msg))
                            break

                        else:
                            bot.send_message(message.chat.id, 'мог и лучше (')
                            msg = []
                            for wt in user_wt:
                                msg.append(wt.question)
                            bot.send_message(message.chat.id, choice(msg))
                            break

                    if all.question == message.text.lower():
                        msg = all.answer.split('|')
                        if len(msg) == 1:
                            bot.send_message(message.chat.id, all.answer)

                            a = [i for i in range(1, 100)]

                            a = choice(a)
                            if a < 20:
                                msg = []
                                for wt in user_wt:
                                    msg.append(wt.question)
                                bot.send_message(message.chat.id, choice(msg))

                        else:
                            bot.send_message(message.chat.id, choice(msg))
                        break

                except RuntimeError:
                    bot.send_message(message.chat.id, 'Ошибка')
                    print('error/text/2_try')

            else:
                for j in user_all:
                    if j.question in message.text.lower().split():

                        for question in message.text.lower().split():
                            question_all = []

                            if question in j.question.split():
                                question_all.append(question)

                            question = ''.join(question_all)

                            if question == j.question:
                                msg = j.answer.split('|')
                                if len(msg) == 1:
                                    bot.send_message(message.chat.id, 'Может ты имел ввиду' + ' ' + j.question + ' ?\n'
                                                     'Тогда: ' +
                                                     '\n' +
                                                     j.answer)

                                    a = [i for i in range(1, 100)]

                                    a = choice(a)
                                    if a < 10:
                                        msg = []
                                        for wt in user_wt:
                                            msg.append(wt.question)
                                            bot.send_message(message.chat.id, 'Может ты имел ввиду' + ' ' + j.question +
                                                             '?\n '
                                                             'Тогда: ' + '\n' +
                                                             choice(msg))
                                            break

                                else:
                                    bot.send_message(message.chat.id, 'Может ты имел ввиду' + ' ' + j.question + ' ?\n'
                                                     'Тогда: ' +
                                                     '\n' +
                                                     choice(msg))
                                break
                        break

                    else:
                        pass
                else:
                    for i in mat:
                        for j in snac:
                            if j in message.text.split():
                                message.text = message.text.replace(j, '')
                                if message.text.lower() == i:
                                    bot.send_message(message.chat.id, 'Пиши без мата, друг )')
                                    start_ht_com(message)
                                    break
                    else:
                        answer_not(message)

        except BaseException:
            bot.send_message(message.chat.id, 'Ошибка')
            print('error/text/1_try')


bot.polling(none_stop=True)
