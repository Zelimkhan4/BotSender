import telebot
from telebot import types
from db_control import *
from utils import generate_markup, generate_base_markup
from sqlalchemy.orm import mapper
import sqlalchemy as sa


API_TOKEN = "1115601017:AAHeOre5a62sLGhNbqVdv_8IQ_fQA9rZdTs"


GROUPS = 'Groups'
RESIDENTS = 'Residents'
SKILLS = 'Skills'
TRACKS = 'Tracks'


class Residents:
    id = sa.Column("id", sa.Integer, primary_key=True)
    pass

class Tracks:
    pass

class Skills:
    pass

class Groups:
    pass







bot = telebot.TeleBot(API_TOKEN)


def phone_handler(message, Resident):
    Resident.phone = message.text
    msg = bot.send_message(message.chat.id, "Регистрация прошла успешно")
    Resident.chatid = message.chat.id
    Resident.username = message.from_user.username
    sess = create_session()
    sess.add(Resident)
    sess.commit()




def ed_handler(message, Resident):
    Resident.ed_place = message.text
    msg = bot.send_message(message.chat.id, "Введите ваш номер телефона")
    bot.register_next_step_handler(msg, phone_handler, Resident)


def skill_handler(message, Resident):
    Resident.role = message.chat.id
    msg = bot.send_message(message.chat.id, "Введите место вашего обучения")
    bot.register_next_step_handler(msg, ed_handler, Resident)

def track_handler(message, Resident):
    Resident.track = message.text
    sess = create_session()
    keyboard = generate_markup(sess.query(METADATA.tables["Skills"]).all())
    msg = bot.send_message(message.chat.id, "Выберите вашу роль", reply_markup=keyboard)
    bot.register_next_step_handler(msg, skill_handler, Resident)


def age_handler(message, Resident):
    Resident.old = message.text
    sess = create_session()
    keyboard = generate_markup(sess.query(METADATA.tables["Tracks"]).all())
    msg = bot.send_message(message.chat.id, "Выбери трек", reply_markup=keyboard)
    bot.register_next_step_handler(msg, track_handler, Resident)

def surname_handler(message, Resident):
    Resident.surname = message.text
    msg = bot.send_message(message.chat.id, "Ваш возраст")
    bot.register_next_step_handler(msg, age_handler, Resident)


def name_handler(message, Resident):
    Resident.name = message.text
    msg = bot.send_message(message.chat.id, "Введите фамилию")
    bot.register_next_step_handler(msg, surname_handler, Resident)





@bot.message_handler(commands=['start'])
def start_message(message):
    user_chat_id = message.chat.id
    sess = create_session()
    bot.send_message(message.chat.id, f'''Здравствуй {message.from_user.first_name}.\n
Я бот для рассылки сообщений.''')
    if not user_chat_id in sess.query(METADATA.tables.get('Residents')).all():
        msg = bot.send_message(message.chat.id, "Введи своё имя")
        new_resident = Residents()
        bot.register_next_step_handler(msg, name_handler, new_resident)
    else:
        bot.send_message(message.chat.id, f'''Здравствуй {message.from_user.first_name}.\n
Я бот для рассылки сообщений.''', reply_markup=generate_base_markup())


@bot.message_handler(content_types=["text"])
def check_message(message):
    if message.text == "Написать группе":
        markup = types.ReplyKeyboardMarkup()
        for i in get_all_groups():
            button = types.KeyboardButton(text=i[0])
            markup.add(button)
        bot.register_next_step_handler(message, send_all_handler)
        bot.send_message(message.chat.id, "Выберите группу", reply_markup=markup)
    elif message.text == "Добавить группу":
        bot.send_message(message.chat.id, "Отлично введите название группы")
        group = Group()
        bot.register_next_step_handler(message, group.name_of_creating_group_handler)


def send_all_handler(message):
    global id_s
    bot.send_message(message.chat.id, "А теперь введите само сообщение", reply_markup=generate_base_markup())
    ids = get_all_id_for_group(message.text)
    bot.register_next_step_handler(message, message_handler)
    id_s = ids

def message_handler(message):
    for i in id_s:
        bot.send_message(i[0], message.text)

if __name__ == '__main__':
    global_init("TeleBotDB.db")   
    mapper(Residents ,METADATA.tables.get("Residents"))
    bot.polling()


