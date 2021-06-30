import telebot
from telebot import types
from data import db_session
from data.__all_models import Resident, Group
from utils import *
import sqlalchemy as sa


API_TOKEN = "1115601017:AAHeOre5a62sLGhNbqVdv_8IQ_fQA9rZdTs"
bot = telebot.TeleBot(API_TOKEN)
BUFFER = set()

def send_message_handler(message):
    global BUFFER
    print(BUFFER)
    for chat_id in BUFFER:
        bot.send_message(chat_id, message.text)
    BUFFER.clear()


def name_search_handler(message):
    name, surname = message.text.split(" ")
    sess = db_session.create_session()
    humans = [(f"{i.name} {i.surname}", i.chat_id) for i in sess.query(Resident).filter(sa.or_(Resident.name == name.lower().capitalize(), Resident.surname == surname.lower().capitalize()))]
    markup = generate_inline_markup(humans)
    msg = bot.send_message(message.chat.id, "Результат поиска", reply_markup=markup)
    bot.register_next_step_handler(msg, send_message_handler)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline_call(call):
    global BUFFER
    msg = None
    if call.data == "Name":
        msg = bot.send_message(call.message.chat.id, "Введите имя и фамилию через пробел")
    elif call.data in ("Role", "Track", "Group"):
        sess = db_session.create_session()
        if call.data == "Role":
            groups = generate_inline_markup([(i.name, f"Group:{i.id}") for i in sess.query(Group).filter(Group.id > 4, Group.id < 9)])
        elif call.data == "Track":
            groups = generate_inline_markup([(i.name, f"Group:{i.id}") for i in sess.query(Group).filter(Group.id > 0, Group.id < 5)])
        else:
            groups = generate_inline_markup([(i.name, f"Group:{i.id}") for i in sess.query(Group).filter(Group.id > 8)])
        msg = bot.send_message(call.message.chat.id, "Роль выбери ле!", reply_markup=groups)
        bot.register_next_step_handler(msg, send_message_handler)
        return
    elif call.data == "All":
        pass
    # Обычный резидент 
    elif call.data.isdigit():
        BUFFER.add(call.data) 
    
    # Группа в формате "Group:{id}"
    elif call.data.startswith("Group"):
        group_id = int(call.data.split(":")[1])
        sess = db_session.create_session()
        for i in sess.query(Resident).all():
            if i.groups.find(f"{group_id}") != -1:
                BUFFER.add(i.chat_id)
    else: 
        return
    if msg is not None:
        bot.register_next_step_handler(msg, name_search_handler)




def skill_handler(message, Resident):
    sess = db_session.create_session()
    skill_id = sess.query(Group.id).filter(Group.name == message.text).first()[0]
    Resident.skill = skill_id
    Resident.groups += f",{skill_id}"
    msg = bot.send_message(message.chat.id, "Регистрация окончена!")
    Resident.chat_id = message.chat.id
    sess.add(Resident)
    sess.commit()    


def track_handler(message, Resident):
    sess = db_session.create_session()
    track_id = sess.query(Group.id).filter(Group.name == message.text).first()[0]
    Resident.track = track_id
    Resident.groups += f"{track_id}"
    keyboard = generate_reply_markup([i[0] for i in sess.query(Group.name).filter(Group.id > 4, Group.id < 10).all()])
    msg = bot.send_message(message.chat.id, "Выберите вашу роль", reply_markup=keyboard)
    bot.register_next_step_handler(msg, skill_handler, Resident)


def surname_handler(message, Resident):
    Resident.surname = message.text
    sess = db_session.create_session()
    groups = [i[0] for i in sess.query(Group.name).filter(Group.id > 0, Group.id < 5).all()]
    keyboard = generate_reply_markup(groups)
    msg = bot.send_message(message.chat.id, "Выберите трек", reply_markup=keyboard)
    bot.register_next_step_handler(msg, track_handler, Resident)


def name_handler(message, Resident):
    Resident.name = message.text
    msg = bot.send_message(message.chat.id, "Введите фамилию")
    bot.register_next_step_handler(msg, surname_handler, Resident)


@bot.message_handler(commands=['start'])
def start_message(message):
    sess = db_session.create_session()
    if not sess.query(Resident).filter(Resident.chat_id == message.chat.id).first():
        msg = bot.send_message(message.chat.id, "Введи своё имя")
        new_resident = Resident()
        new_resident.groups = ""
        bot.register_next_step_handler(msg, name_handler, new_resident)
    else:
        bot.send_message(message.chat.id, f'''Здравствуй {message.from_user.first_name}.\n
Я бот для рассылки сообщений.''', reply_markup=generate_base_markup())



if __name__ == '__main__':
    db_session.global_init("TeleBot.db")
    bot.polling()


