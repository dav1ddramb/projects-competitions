import telebot
import time
import requests
import numpy as np
import re
from telebot import types
from bs4 import BeautifulSoup


bot = telebot.TeleBot(token='1076104051:AAHJuSRQUgGPNFUjjLXe3qN1g93-UK5cLis')

# markup = types.ReplyKeyboardMarkup(row_width=2)
# itembtn1 = types.KeyboardButton('/get_meme')
# markup.add(itembtn1)

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('/titanic')
markup.add(itembtn1)


# from telebot.types import ReplyKeyboardMarkup
# from telebot.types import KeyboardButton
# from telebot.types import KeyboardButtonPollType
# from telebot.types import ReplyKeyboardRemove
#
# poll_markup = ReplyKeyboardMarkup(one_time_keyboard=True)
# poll_markup.add(KeyboardButton('send me a poll', request_poll=KeyboardButtonPollType(type='quiz')))
# remove_board = ReplyKeyboardRemove()
# bot.send_message(chat_id,text,reply_markup=poll_markup)

def get_url():
    req = requests.Session()
    contents = req.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    return image_url

def listener(messages):
    for m in messages:
        chatid = m.chat.id
        if m.content_type == 'text':
            text = m.text
            #bot.send_message(chatid, text)
            return text


### TITANIC DATASET TUTORIAL ###


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    # reply_to
    bot.send_message(chat_id=chat_id,
                     text='Привет!'
                          '\nСейчас ты увидишь, как интересно и просто работать с данными, и мы вместе построим модель '
                          'машинного обучения, которая будет предсказывать, *выжил ли пассажир Титаника* '
                          '\n'
                          '\nПросто нажми /titanic и ничего не бойся!',
                     parse_mode='Markdown'
                     )


@bot.message_handler(commands=['titanic'])
def titanic(message):
    tit_url = 'https://drive.google.com/file/d/1ntvOr2pQ3ijQg9oM-QvylW7dKO31Pa0c/view?usp=sharing'
    tit_url = open('titanic01.png', 'rb')
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='Взглянем на _данные о пассажирах Титаника_.'
                          '\nДа, это реальные данные о реальных людях на корабле'
                          '\n'
                          '\nКаждая строка — один пассажир. Пока это больше похоже на кашу. '
                          '\nНо скоро мы со всем разберемся!',
                     parse_mode="Markdown"
                     )
    bot.send_photo(chat_id=chat_id, photo=tit_url)

    bot.send_message(chat_id=chat_id,
                     text='Описание столбцов(или _признаков_): '
                          '\n*Survived* - факт выживания (_1 - выжил, 0 - нет_)'
                          '\n*Pclass* - класс кабины пассажира (чем меньше, тем круче)'
                          '\n*Name* - имя пассажира'
                          '\n*Sex* - пол пассажира'
                          '\n*Age* - возраст пассажира'
                          '\n*SibSp* - кол-во братьев/сестер/супругов пассажира на борту Титаника'
                          '\n*Parch* - кол-во родителей/детей пассажира на борту Титаника'
                          '\n*Ticket* - номер билета'
                          '\n*Fare* - стоимость билета пассажира'
                          '\n*Cabin* - номер кабины'
                          '\n*Embarked* - порт посадки (_C = Cherbourg, Q = Queenstown, S = Southampton_)',
                     parse_mode="Markdown")

    bot.send_message(chat_id=chat_id, text='Нажми /clear_data чтобы почистить данные', parse_mode="html")


@bot.message_handler(commands=['clear_data'])
def clear_data(message):
    tit_url = 'https://drive.google.com/file/d/1guuzARWxY5OwP9OXE1Njp-0Q7HJ_37rA/view?usp=sharing'
    tit_url = open('titanic02.png', 'rb')
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='Как думаешь, какие из этих столбцов могут быть <b>бесполезны</b> при определении выживания пассажира?'
                          '\nПодумай сам, прежде чем смотреть на ответ. Какие столбцы не влияют на <b>Survived</b> логически?'
                          '\n'
                          '\n<b>Ответ: </b>'
                          '\n<b>Name</b> — действительно, Джон и Джек замерзают в воде одинаково'
                          '\n<b>Ticket</b> — это вообще просто набор знаков — в помойку его'
                          '\n<b>Cabin</b> — аналогично'
                          '\n<i>Выбросим их все из данных</i>'
                          '\n'
                          '\n<b>Спорные моменты: </b>'
                          '\nВлияние некоторых признаков очень спорное. Но на вcякий случай оставим их, всегда поступай так :)'
                          '\nЖми /clear_explain чтобы посмотреть на объяснение',
                     parse_mode="html")
    bot.send_photo(chat_id=chat_id, photo=tit_url)
    bot.send_message(chat_id=chat_id, text='Жми /encode чтобы продолжить', parse_mode="html")


@bot.message_handler(commands=['clear_explain'])
def clear_explain(message):
    tit_url = 'https://drive.google.com/file/d/1f2DLt5A5xjK8t8ejKfozMmNdkfFihk96/view?usp=sharing'
    tit_url = open('titanic03.png', 'rb')
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='Почему мы оставили те признаки, которые оставили?'
                          '\n'
                          '\n<b>Survived</b> - это наша <b>целевая переменная</b> '
                          '— то, что мы будем предсказывать'
                          '\n<b>Pclass</b> - более статусных пассажиров могли  спасать первыми'
                          '\nКак и более богатых, <b>Fare</b> может говорить об этом'
                          '\nЖенщин спасали первыми, так что <b>Sex</b> остается'
                          '\nКак и детей, <b>Age</b> - возраст тоже'
                          '\n'
                          '\nОстались наиболее спорные: '
                          '\nЧем больше родственников, тем больше шанс, что тебя кто-то '
                          'захочет спасти. Оставим <b>SibSp</b> и <b>Parch</b> на  всякий случай.'
                          '\nТа же история и с <b>Embarked</b>. Может, в одном порту были более '
                          'богатые пассажиры, а может и нет. Знать этого точно не можем, '
                          'но сильно погоды это не испортит, оставляем!',
                     parse_mode="html")

    bot.send_photo(chat_id=chat_id,
                   photo=tit_url,
                   caption='Ах да, насчет спасения женщин и детей'
                           '\nКак видишь, женщин и правда спаслось немало'
                   )
    bot.send_message(chat_id=chat_id,
                     text='Жми /encode чтобы продолжить',
                     parse_mode="html")


@bot.message_handler(commands=['encode'])
def encode(message):
    tit_url = 'https://drive.google.com/file/d/1bZJpXcnQdYWCZ6y487o6KlHEh79O66Kv/view?usp=sharing'
    tit_url = open('titanic04.png', 'rb')
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='Мы почистили данные. Теперь из <b>букв</b> сделаем <b>числа</b>.'
                          '\nЭто нужно для построения модели. Ты же не сможешь умножить <i>\"male\"</i> на 10. Или сможешь?)'
                          '\n'
                          '\nПрименим для этого метод <a href="https://hackernoon.com/what-is-one-hot-encoding-why-and-when-do-you-have-to-use-it-e3c6186d008f"><i>one-hot-encoding</i></a>'
                          '\n'
                          '\nНапример, <i>\"male\"</i> и <i>\"female\"</i> в <b>Sex</b> поменяем на 1 для мужчин и 0 для женщин'
                          '\nПохоий подход для <b>Embarked</b>, но вместо одного столбца придется сделать 3 - для каждого из портов',
                     parse_mode="html",
                     disable_web_page_preview=True)

    bot.send_photo(chat_id=chat_id,
                   photo=tit_url,
                   caption='Получаем такие  обработанные данные по пассажирам: '
                           '\n'
                           '\n<b>male</b> = 1 для мужчин'
                           '\n<b>Emb_C, Emb_Q, Emb_S</b> = 1 для соответствующего порта'
                           '\n'
                           '\nПРОВЕРКА: Для каждой строки(пассажира) 1 может быть только в одном из этих трех полей',
                   parse_mode="html")

    bot.send_message(chat_id=chat_id,
                     text='Жми /plot . Добрались до интересного :)',
                     parse_mode="html")


## PLOT ##
# COLORS for plt.hist()% https://matplotlib.org/stable/gallery/color/named_colors.html
@bot.message_handler(commands=['plot'])
def plot(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='Распределение каких признаков хочешь посмотреть: '
                          '\n/plot1 <b>SibSp</b> и <b>Parch</b>'
                          '\n/plot2 <b>Pclass</b> и <b>Fare</b>'
                          '\n/plot3 <b>Sex</b> и <b>Age</b>'
                          '\n/plot4 <b>порт_посадки</b> и <b>Survived</b>'
                          '\n'
                          '\nЖми /model чтобы отправиться к построению модели',
                     parse_mode="html",
                     disable_web_page_preview=True)


@bot.message_handler(commands=['plot1'])
def plot1(message):
    tit_url = open('titanic05.png', 'rb')
    chat_id = message.chat.id

    bot.send_photo(chat_id=chat_id,
                   photo=tit_url,
                   caption='Посмотреть другое распределение: '
                           '\n/plot2'
                           '\n/plot3'
                           '\n/plot4'
                           '\nИли жми /model чтобы отправиться к построению модели',
                   parse_mode="html")

@bot.message_handler(commands=['plot2'])
def plot2(message):
    tit_url = open('titanic06.png', 'rb')
    chat_id = message.chat.id

    bot.send_photo(chat_id=chat_id,
                   photo=tit_url,
                   caption='Посмотреть другое распределение: '
                           '\n/plot1'
                           '\n/plot3'
                           '\n/plot4'
                           '\nИли жми /model чтобы отправиться к построению модели',
                   parse_mode="html")

@bot.message_handler(commands=['plot3'])
def plot3(message):
    tit_url = open('titanic07.png', 'rb')
    chat_id = message.chat.id

    bot.send_photo(chat_id=chat_id,
                   photo=tit_url,
                   caption='Посмотреть другое распределение: '
                           '\n/plot1'
                           '\n/plot2'
                           '\n/plot4'
                           '\nИли жми /model чтобы отправиться к построению модели',
                   parse_mode="html")

@bot.message_handler(commands=['plot4'])
def plot4(message):
    tit_url = open('titanic08.png', 'rb')
    chat_id = message.chat.id

    bot.send_photo(chat_id=chat_id,
                   photo=tit_url,
                   caption='Посмотреть другое распределение: '
                           '\n/plot1'
                           '\n/plot2'
                           '\n/plot3'
                           '\nИли жми /model чтобы отправиться к построению модели',
                   parse_mode="html")

####


@bot.message_handler(commands=['model'])
def model(message):
    chat_id = message.chat.id
    bot.send_message(chat_id=chat_id,
                     text='Наша модель должна по выбранным столбцам-признакам '
                          'предсказывать выживет пассажир или нет: 1 или 0.'
                          '\n'
                          '\nПрименим для этого <a href="https://towardsdatascience.com/introduction-to-logistic-regression-66248243c148"><i>логистическую регрессию</i></a>'
                          ' (<a href="https://habr.com/ru/company/ods/blog/323890/#2-logisticheskaya-regressiya"><i>более сложное объяснение, но на русском</i></a>)',
                     parse_mode="html")



@bot.message_handler(func=lambda msg: msg.text is not None)
def answer(message):
    url = get_url()
    chat_id = message.chat.id
    text = message.text
    bot.reply_to(message, '{} - такой команды я еще не знаю. Не засоряй меня, пожалуйста)'.format(text))

    # chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id,
                   photo=url,
                   caption='Этот блок еще не готов, так что лови песеля',
                   parse_mode="html")



#bot.set_update_listener(listener)

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15) 