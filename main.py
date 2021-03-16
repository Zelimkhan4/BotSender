import telebot
import config
from db_control import add_new_row, get_data, get_tracks_name
import sqlite3



# Базовая клавиатура для бота
base_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
base_markup.add(telebot.types.KeyboardButton('Просмотреть все группы', ))
base_markup.add(telebot.types.KeyboardButton('Добавить группу'))
base_markup.add(telebot.types.KeyboardButton('Редактировать группу'))


# Класс бота
class Bot(telebot.TeleBot):
    def __init__(self, apikey):
        super().__init__(apikey)
        self.name = "бот для рассылки"
        self.creator = "Last Dark Emperor of Galactic Empire"
        self.markup = base_markup
        self.con = sqlite3.connect("TelebotDB.db")
        self.data = {}
    

bot = Bot(config.apikey)

# Класс группы
class Group:
    def __init__(self, name, participants):
        self.name = name
        self.participants = participants

    def add_participant(self, participant):
        self.participants.append(participant)

    def get_info(self):
        return  'Name of group: ' + self.name + '\n' + "\n".join(i.get_info() for i in self.participants)



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
        mark = telebot.types.InlineKeyboardMarkup(row_width=len(tracks))
        print(tracks)
        for i in tracks:
            mark.add(telebot.types.InlineKeyboardButton(i[0], callback_data=i[0]))
        msg = bot.send_message(message.chat.id, "Введите свой трек", reply_markup=mark)
        bot.register_next_step_handler(msg, self.track_handler)

    def track_handler(self, message):
        self.track = message.text
        msg = bot.send_message(message.chat.id, "Введите вашу специализацию")
        bot.register_next_step_handler(msg, self.role_handler)

    def role_handler(self, message):
        self.role = message.text
        msg = bot.send_message(message.chat.id, "Введите ваше место обучения")
        bot.register_next_step_handler(msg, self.ed_handler)
    
    def ed_handler(self, message):
        self.ed_place = message.text
        bot.send_message(message.chat.id, "Регистрация окончена товарищ")
        self.add_new_row(message)

    def add_new_row(self, message):
        con = sqlite3.connect("TelebotDB.db")
        print(self.name, self.surname, self.old, self.ed_place, self.role, self.rank)
        con.execute(f"""INSERT INTO Residents ('username', 'chatid', 'name', 'surname', 'old', 'track', 'role', 'ed_place')
                        VALUES ('{message.from_user.username}', '{message.chat.id}', '{self.name}', '{self.surname}', {self.old}, '{self.track}', '{self.role}', '{self.ed_place}')""")
        con.commit()


# names = {'Zelimkhan': {'number':'89991429243',
#                          'profession': 'Programmer',
#                          'rank': 0,
#                          'track': 'Innovator',
#                          'ed_place': 'shkola',
#                          'old': 3000},
#         'Aishat': {'number': '89282690871',
#                          'profession': 'Designer',
#                          'rank': 2,
#                          'track': 'Activist',
#                          'ed_place': 'shkola',
#                          'old': 22},
#         'Samad': {'number': '89626564991',
#                          'profession': 'Unreal Dev',
#                          'rank': 4,
#                          'track': 'Innovator',
#                          'ed_place': 'shkola',
#                          "old": 16},
#         "Deni": {'number': '89383526230',
#                          'profession': 'Project Manager',
#                          'rank': 4,
#                          'track': 'Proektirovshik',
#                          'old': 21,
#                          'ed_place': 'shkola'}}





@bot.callback_query_handler(func=lambda call: True)
def handle_button(call):
    bot.send_message(call.message.chat.id, call.data)
    

@bot.message_handler(commands=['send_all'])
def send_all_messages(message):
    con = sqlite3.connect('TeleBotDB.db')
    cur = con.cursor()
    ids = cur.execute('''SELECT ChatId FROM Residents''').fetchall()
    for id in ids:
        bot.send_message(id[0], 'Hello world')   




# Обработчик start
# C него начинаем наш опрос
@bot.message_handler(commands=['start'])
def start_message(message):
    user = Contact()
    bot.send_message(message.chat.id, f'''Здравствуй {message.from_user.first_name}.\n
Я бот для рассылки сообщений.''', reply_markup=bot.markup)
    if not get_data(f"""SELECT chatid from Residents WHERE username = '{message.from_user.username}'""").fetchall():  
        msg = bot.send_message(message.chat.id, "Введи своё имя")
        bot.register_next_step_handler(msg, user.name_handler)




# @bot.message_handler(content_types=['text'])
# def send_message(message):
#     bot.send_message(message.chat.id, "send_to")

if __name__ == '__main__':
    bot.polling()