import telebot
from telebot import types
import config
from db_control import *
import sqlite3
from utils import generate_markup, generate_base_markup
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
id_s = None


GROUPS = 'Groups'
RESIDENTS = 'Residents'
SKILLS = 'Skills'
TRACKS = 'Tracks'


# Класс бота
class Bot(telebot.  TeleBot):
    def __init__(self, apikey):
        super().__init__(apikey)
        self.name = "бот для рассылки"
        self.creator = "Last Dark Emperor of Galactic Empire"
        self.markup = generate_base_markup()
        self.con = sqlite3.connect("TelebotDB.db")
        self.data = {}
    

bot = Bot(API_TOKEN)


# Класс группы
class Group:
    def __init__(self):
        self.name = None
        self.participants = []

    def add_participant(self, participant):
        self.participants.append(participant)

    def get_info(self):
        return  'Name of group: ' + self.name + '\n' + "\n".join(i.get_info() for i in self.participants)

    def name_of_creating_group_handler(self, message):
        kb = types.ReplyKeyboardMarkup()
        kb.row_width = 2
        for name, surname in get_all_residents():
            kb.add(types.KeyboardButton(name + " " + surname))
        kb.add(types.KeyboardButton('Stop'))
        self.name = message.text
        bot.register_next_step_handler(message, self.participants_adding_handler)
        bot.send_message(message.chat.id, "А теперь выберите участников.", reply_markup=kb)

    def participants_adding_handler(self, message):
        if message.text == "Stop":
            add_new_group(self.name, self.participants)
        self.participants.append(message.text)
        bot.register_next_step_handler(message, self.participants_adding_handler)


class Contact:
    def __init__(self):
        self.name = None
        self.surname = None
        self.number = None
        self.profession = None
        self.rank = None
        self.track = None
        self.old = None
        self.ed_place = None
        self.role = None

    def get_info(self):
        return f"Вы: Имя: {self.name}\nФамилия: {self.surname}\nТрек: {self.track}"

    def name_handler(self, message):
        self.name = message.text
        msg = bot.send_message(message.chat.id, "Введите свою фамилию")
        bot.register_next_step_handler(msg, self.surname_handler)

    def surname_handler(self, message):
        self.surname = message.text
        msg = bot.send_message(message.chat.id, "Введите свой возраст")
        bot.register_next_step_handler(msg, self.age_handler)
    
    def age_handler(self, message):
        self.old = message.text
        tracks = get_tracks_name()
        mark = generate_markup(tracks)
        msg = bot.send_message(message.chat.id, "Выберите свой трек", reply_markup=mark)
        bot.register_next_step_handler(msg, self.track_handler)

    def track_handler(self, message):
        self.track = message.text
        profs = get_proffessions()
        mark = generate_markup(profs)
        msg = bot.send_message(message.chat.id, "Выберите вашу специализацию", reply_markup=mark)
        bot.register_next_step_handler(msg, self.role_handler)

    def role_handler(self, message):
        self.role = message.text
        msg = bot.send_message(message.chat.id, "Введите ваше место обучения")
        bot.register_next_step_handler(msg, self.ed_handler)
    
    def ed_handler(self, message):
        self.ed_place = message.text
        bot.send_message(message.chat.id, "Регистрация окончена товарищ", reply_markup=generate_base_markup())
        self.add_new_resident(message)

    def add_new_resident(self, message):
        con = sqlite3.connect("TelebotDB.db")
        groups = con.execute(f"SELECT id FROM Groups WHERE name in ('{self.track}', '{self.role}')").fetchall()
        groups = tuple([i[0] for i in groups])
        con.execute(f"""INSERT INTO Residents ('username', 'chatid', 'name', 'surname', 'old', 'track', 'role', 'ed_place', 'groups')
                        VALUES ('{message.from_user.username}', '{message.chat.id}', '{self.name}', '{self.surname}', {self.old},
                        (SELECT id from Tracks WHERE name = '{self.track}'),
                        (SELECT id FROM Skills WHERE name = '{self.role}'), '{self.ed_place}', '{groups}')""")
        con.commit()
        self.instances.append(self)




# Обработчик start
# C него начинаем наш опрос
@bot.message_handler(commands=['start'])
def start_message(message):
    user = Contact()
    if not get_data(f"""SELECT chatid from Residents WHERE chatid = '{message.chat.id}'""").fetchall():  
        bot.send_message(message.chat.id, f'''Здравствуй {message.from_user.first_name}.\n
Я бот для рассылки сообщений.''')
        msg = bot.send_message(message.chat.id, "Введи своё имя")
        bot.register_next_step_handler(msg, user.name_handler)
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
    global_init('TeleBotDB.db')
    bot.polling()