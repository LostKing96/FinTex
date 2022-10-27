#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Bauyrzhan Ospan"
__copyright__ = "Copyright 2019"
__version__ = "1.0.1"
__maintainer__ = "Beksultan Maukenov"
__email__ = "bmaukenov@gmail.com"
__status__ = "Development"

import telebot
from telebot import types
from pprint import pprint
import logging
from pymongo import MongoClient
import pymongo
import datetime
import time


# region: Constants
client = MongoClient('mongodb://database:27017/')
db = client['FinTEx_tlg_bot']
col_names = db.list_collection_names()
users = db['users']
u_log = db['log']
messages = db['messages']
settings = db['settings']

if settings.find_one():
    setting = settings.find_one()
else:
    default_settings = {
        "ID админа": "Можно группы (в начале -), но в начале сделайте бота админом в группе",
        "Hash бота": "5250208414:AAGITAI1ORwWrAGX3d7-ASxJLSKGNOKuw84",
        "Собирать контакты пользователей?": True,
        "Текст для сообщения регистрации": "Пройдите регистрацию: укажите свой номер",
        "Текст ошибки": "Простите, бот сломался"
        }
    settings.insert_one(default_settings)
    hello_strings = [{
        "level": 0,
        "button": "Домой",
        "text": "Выберите в меню то, что вас интересует",
        "parent": -1,
        "children": [10, 20, 30, 40, 50, 60]
        },
        {
        "level": 10,
        "button": "Полезные ссылки",
        "text": "Посмотрите в меню много полезных ссылок для вас",
        "parent": 0,
        "children": [110, 210, 310, 410, 510]
        },
        {
        "level": 20,
        "button": "Вопрос по вашему проекту",
        "text": "Выберите в меню свой вопрос",
        "parent": 0,
        "children": [120, 220, 320, 420, 520]
        },
        {
        "level": 110,
        "button": "Уроки",
        "text": "Вот ссылка на [курс.](https://fintex.kz/authorized/zero_lesson)",
        "parent": 10,
        "children": []
        },
        {
        "level": 210,
        "button": "Раздаточный материал",
        "text": "Вот ссылка на [раздаточный материал](https://drive.google.com/drive/folders/1gmTePB63C4U2WvV3n-7mhABCwmlYMIpI?usp=sharing)",
        "parent": 10,
        "children": []
        },
        {
        "level": 310,
        "button": "Требования для подачи",
        "text": "Ловите список необходимых [документов для подачи](https://drive.google.com/file/d/1XR07Asw_vpOBPFGW7t8xB-dwVZekeRsN/view?usp=sharing)",
        "parent": 10,
        "children": []
        },
        {
        "level": 410,
        "button": "Что такое новизна идеи?",
        "text": "Подготовили для вас [критерии новизны идеи](https://drive.google.com/file/d/1TK8IfZuGYdkAxPRcvCoUH_4tb6BN6F61/view?usp=sharing)",
        "parent": 10,
        "children": []
        },
        {
        "level": 510,
        "button": "Соц. уязвимые слои населения",
        "text": "Посмотрите список с описанием [соц. уязвимых слоев населения](https://docs.google.com/document/d/1_NpJjzmgFXduBdGjVcZWKV5K2pMVnFvB2Uhs9EsJSqs/edit)",
        "parent": 10,
        "children": []
        },
        {
        "level": 120,
        "button": "Вопрос по идее",
        "text": "Выберите в списке ваш вопрос",
        "parent": 20,
        "children": [1120, 2120, 3120]
        },
        {
        "level": 1120,
        "button": "Подходит ли моя идея?",
        "text": "Если хотите узнать, подходит ли Ваша идея - проверьте по [чеклисту новизны идеи](https://drive.google.com/file/d/1TK8IfZuGYdkAxPRcvCoUH_4tb6BN6F61/view?usp=sharing)",
        "parent": 120,
        "children": []
        },
        {
        "level": 2120,
        "button": "Подходит ли мой ОКЭД?",
        "text": "ОКЭД - это код сферы бизнеса. В гранте можно участвовать только по проектам с определенными сферами бизнеса. Ловите [список разрешенных ОКЭДов](https://drive.google.com/file/d/1pEMkqxvXcxrHF1vHaaoI-wEoOYFJAhB6/view?usp=sharing)",
        "parent": 120,
        "children": []
        },
        {
        "level": 3120,
        "button": "Как сделать инновацию?",
        "text": " Чтобы сделать свою идею инновационной, посмотрите посвященный этому [видео урок](https://fintex.kz/authorized/first_lesson)",
        "parent": 120,
        "children": []
        },
        {
        "level": 220,
        "button": "Вопрос по документам",
        "text": "Ловите список необходимых [документов для подачи](https://drive.google.com/file/d/1XR07Asw_vpOBPFGW7t8xB-dwVZekeRsN/view?usp=sharing)",
        "parent": 20,
        "children": []
        },
        {
        "level": 320,
        "button": "Вопрос по бизнес плану",
        "text": "Выберите ваш вопрос из списка",
        "parent": 20,
        "children": [1320, 2320]
        },
        {
        "level": 1320,
        "button": "Как сделать анализ рынка",
        "text": "Чтобы узнать, как сделать анализ рынка, посмотрите видеоуроки из нашего курса - [2 урок](https://fintex.kz/authorized/second_lesson) и [3 урок](https://fintex.kz/authorized/third_lesson)",
        "parent": 320,
        "children": []
        },
        {
        "level": 2320,
        "button": "Что такое бизнес модель?",
        "text": "Вот ссылка на самые распространенные [бизнес модели](https://drive.google.com/file/d/1pxq5zqsC3vPfibZ7LWayabLzFEBbtUip/view?usp=sharing)",
        "parent": 320,
        "children": []
        },
        {
        "level": 420,
        "button": "Вопрос по фин модели",
        "text": "Если у вас есть вопросы по финансовой модели, посмотрите наш [4 урок по фин. модели](https://fintex.kz/authorized/fourth_lesson)",
        "parent": 20,
        "children": []
        },
        {
        "level": 520,
        "button": "У меня штрафы и задолженности",
        "text": "При подаче смотрят только на налоговые задолженности. Если их нет, то подавать можно.",
        "parent": 20,
        "children": []
        },
        {
        "level": 30,
        "button": "Нужна индивидуальнуя консультация",
        "text": "Эта услуга платная. Записаться на консультацию вы можете по этой [ссылке](https://fintex.kz/authorized/marafon)",
        "parent": 0,
        "children": []
        },
        {
        "level": 40,
        "button": "Бизнес план на проверку",
        "text": "Чтобы отправить бизнес план на проверку, напишите в Телеграм нашему менеджеру Акторе. Его аккаунт в Телеграм - (@fintexme), номер телефона (только в Телеграм): +7 775 914 29 75",
        "parent": 0,
        "children": []
        },
        {
        "level": 50,
        "button": "Грант Бастау",
        "text": "Вот вам официальный государственный [документ о программе Бастау](https://adilet.zan.kz/rus/docs/P1800000746). Посмотрите пункт 5.2.5",
        "parent": 0,
        "children": []
        },
        {
        "level": 60,
        "button": "FAQ",
        "text": "Выберите свой вопрос из списка",
        "parent": 0,
        "children": [160, 260, 360, 460, 560, 660, 760, 860, 960, 1060]
        },
        {
        "level": 160,
        "button": "Для кого грант 5 млн. тенге?",
        "text": "Есть три категории:\n-Начинающие предприниматели (ИП/ТОО до трех лет)\n-Молодые начинающие предприниматели (директору менее 29 лет)\n-Малый бизнес (работники до 100чел., оборот менее 300 000 МРП)",
        "parent": 60,
        "children": []
        },
        {
        "level": 260,
        "button": "Могу ли я получить грант 5 млн. тенге если получала грант Бастау (500 тыс. тенге)?",
        "text": "Да, в таком порядке можно. Наоборот (нужно сперва 5 млн.тг., потом Бастау грант) нельзя. ",
        "parent": 60,
        "children": []
        },
        {
        "level": 360,
        "button": "Могу ли я участвовать с “классическим бизнесом” или с такой идеей?",
        "text": "К сожалению, нет. Проект/идея должна быть инновационной или новой для Вашего региона. Если добавите какой-то новый и/или инновационный элемент (онлайн услуги, новая технология, оборудование и тд.), то можно. Главное чтобы ОКЭД (код направления бизнеса) соответствовал критериям.",
        "parent": 60,
        "children": []
        },
        {
        "level": 460,
        "button": "Мне 50+ лет, могу участвовать?",
        "text": "Да, конечно! Возраст не помеха.",
        "parent": 60,
        "children": []
        },
        {
        "level": 560,
        "button": "Я студент, могу получить грант?",
        "text": "Конечно да, главное подготовиться.",
        "parent": 60,
        "children": []
        },
        {
        "level": 660,
        "button": "Сертификат от Атамекена нужен в это году?",
        "text": "В этом году Акимат Астаны сказал что не нужен, от других Акиматов ожидаем инфу. Если в одном нет, то скорее всего и в остальных не нужен. В Атамекене но смогли многие отучиться, они не успевали записаться, поэтому скорее всего и отменят.",
        "parent": 60,
        "children": []
        },
        {
        "level": 760,
        "button": "Когда начнется конкурс/прием документов?",
        "text": "Зависит от региона, и когда им поступят средства для конкурса. По нашим источникам первые объявления появятся уже в феврале в Павлодарской, Акмолинской областях, Кокшетау и Уральск. В Астане, Алмате и Алматинской области объявят в марте.",
        "parent": 60,
        "children": []
        },
        {
        "level": 860,
        "button": "Сколько нужно денег для участия?",
        "text": "Участие бесплатно, но нужно софинансирование минимум 10% (то есть 500 000 тенге)",
        "parent": 60,
        "children": []
        },
        {
        "level": 960,
        "button": "У меня нет ИП/ТОО более 5 лет, могу участвовать?",
        "text": "Если вы подпадаете под категорию малого бизнеса (сотр.<100, оборот<300 000 МРП.), то можете в Астане точно, в других городах скорее всего да, но на всякий можете уточнить в Управление Предпринимательства вашего региона.",
        "parent": 60,
        "children": []
        },
        {
        "level": 1060,
        "button": "На рекламу можно тратить деньги с гранта?",
        "text": "Да.",
        "parent": 60,
        "children": []
        }
    ]
    messages.insert_many(hello_strings)

setting = settings.find_one()
bot = telebot.TeleBot(setting["Hash бота"])
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
group_id = setting["ID админа"]
collect_phone = setting["Собирать контакты пользователей?"]
phone_collect_text = setting["Текст для сообщения регистрации"]
# endregion


# region: Функции работы
def send_answer(msg, message):
    text = msg["text"]
    parent = msg["parent"]
    child = msg["children"]
    buttons = []
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)

    if len(child) > 0:
        for c in child:
            buttons.append(types.KeyboardButton(str(messages.find_one({"level": c})["button"])))

    if parent != -1:
        buttons.append(types.KeyboardButton("Назад: " + str(messages.find_one({"level": parent})["button"])))

    buttons.append(types.KeyboardButton(str(messages.find_one({"level": 0})["button"])))

    for button in buttons:
        markup.add(button)

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode= 'Markdown')

def find_msg(message):
    button = message.text
    if len(button.split("азад: ")) > 1:
        try:
            return messages.find_one({"button": button.split("зад: ")[1]})
        except:
            return False
    else:
        try:
            return messages.find_one({"button": button})
        except:
            return False

def send_error(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    markup.add(types.KeyboardButton(str(messages.find_one({"level": 0})["button"])))
    bot.send_message(message.chat.id, str(setting["Текст ошибки"]), reply_markup=markup, parse_mode= 'Markdown')
# endregion


# Приветсвие
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if collect_phone:
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        reg_button = types.KeyboardButton(text="Пройти регистрацию", request_contact=True)
        keyboard.add(reg_button)
        user = {
            "user": str(message.chat.id),
            "firstname": str(message.chat.first_name),
            "lastname": str(message.chat.last_name),
            "username": str(message.chat.username),
            "registration": message.date,
            "phone": "",
            }
        users.insert_one(user)
        bot.send_message(message.chat.id, phone_collect_text, reply_markup=keyboard, parse_mode= 'Markdown')
    else:
        try:
            send_answer(messages.find_one({"level": 0}), message)
        except:
            bot.send_message(message.chat.id, "Бот еще не настроен для работы", parse_mode= 'Markdown')


# Сбор контакта
@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    if message.contact is not None:
        if users.count_documents({"user": str(message.chat.id)})>0:
            users.update_one({"user": str(message.chat.id)}, { "$set": { "phone": str(message.contact.phone_number)}})
            send_answer(messages.find_one({"level": 0}), message)
        else:
            user = {
                "user": str(message.chat.id),
                "firstname": str(message.chat.first_name),
                "lastname": str(message.chat.last_name),
                "username": str(message.chat.username),
                "registration": message.date,
                "phone": str(message.contact.phone_number)
                }
            users.insert_one(user)
            send_answer(messages.find_one({"level": 0}), message)
    else:
        hello_string = 'Регистрация обязательна'
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        reg_button = types.KeyboardButton(text="Пройти регистрацию", request_contact=True)
        keyboard.add(reg_button)
        bot.send_message(message.chat.id, hello_string, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    log_m = {
        "from": str(message.chat.id),
        "time": message.date,
        "message": message.text
        }
    u_log.insert_one(log_m)
    
    msg = find_msg(message)

    if msg == False:
        send_error(message)
    else:
        send_answer(msg, message)


if __name__ == "__main__":
    bot.polling()