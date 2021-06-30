import telebot
from telebot import types
from data import db_session
from data.__all_models import Resident, Group
from utils import generate_markup, generate_base_markup
from sqlalchemy.orm import create_session, mapper
import sqlalchemy as sa


API_TOKEN = "1115601017:AAHeOre5a62sLGhNbqVdv_8IQ_fQA9rZdTs"
bot = telebot.TeleBot(API_TOKEN)


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
    Resident.groups += f",{track_id}"
    keyboard = generate_markup(sess.query(Group.name).filter(Group.id > 4, Group.id < 10).all())
    msg = bot.send_message(message.chat.id, "Выберите вашу роль", reply_markup=keyboard)
    bot.register_next_step_handler(msg, skill_handler, Resident)


def surname_handler(message, Resident):
    Resident.surname = message.text
    sess = db_session.create_session()
    groups = sess.query(Group.name).filter(Group.id > 0, Group.id < 5).all()
    keyboard = generate_markup(groups)
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


