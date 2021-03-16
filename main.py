import telebot
import config
from db_control import add_new_row, get_data
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
        msg = bot.reply_to(message, "Введите свою фамилию")
        bot.register_next_step_handler(msg, self.surname_handler)

    def surname_handler(self, message):
        self.surname = message.text
        msg = bot.reply_to(message, "Введите свой возраст")
        bot.register_next_step_handler(msg, self.age_handler)
    
    def age_handler(self, message):
        self.old = message.text
        msg = bot.reply_to(message, "Введите свой трек")
        bot.register_next_step_handler(msg, self.track_handler)

    def track_handler(self, message):
        self.track = message.text
        msg = bot.reply_to(message, "Введите вашу специализацию")
        bot.register_next_step_handler(msg, self.role_handler)

    def role_handler(self, message):
        self.role = message.text
        msg = bot.reply_to(message, "Введите ваше место обучения")
        bot.register_next_step_handler(msg, self.ed_handler)
    
    def ed_handler(self, message):
        self.ed_place = message.text
        bot.send_message(message.chat.id, "Регистрация окончена товарищ")
        self.create_new_contact(message)

    def create_new_contact(self, message):
        con = sqlite3.connect("TelebotDB.db")
        print(self.name, self.surname, self.old, self.ed_place, self.role, self.rank)
        con.execute(f"""INSERT INTO Residents ('username', 'chatid', 'name', 'surname', 'old', 'track', 'role', ed_place)
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
        msg = bot.reply_to(message, "Введи своё имя")
        bot.register_next_step_handler(msg, user.name_handler)

@bot.callback_query_handler(func=lambda call: True)
def print_group_info(call):
    # for group in groups:
    #     if call.data == 'view_' + group.name:
    #         bot.send_message(call.message.chat.id, group.get_info())
    #         break
    #     elif call.data == 'edit_' + group.name:
    #         markup = telebot.types.ReplyKeyboardMarkup()
    #         features = ['Add member', 'Remove member', 'Edit member']
    #         for f in features:
    #             button = telebot.types.InlineKeyboardButton(f, callback_data='edit_' + f + group.name)
    #             markup.add(button)
    #         bot.send_message(call.message.chat.id, 'Что вы хотите сделать?', reply_markup=markup)
    bot.send_message('send_to')


@bot.message_handler(content_types=['text'])
def send_message(message):
    # markup = telebot.types.InlineKeyboardMarkup()
    # if message.text == 'Просмотреть все группы':
    #     for group in groups:
    #         button = telebot.types.InlineKeyboardButton(text=group.name, callback_data='view_' + group.name)
    #         markup.add(button)


    #     bot.send_message(message.chat.id, f'Выберите одну из групп:', reply_markup=markup)

    # if message.text == "Добавить группу":
    #     bot.send_message(message.chat.id, 'Отлично введи название группы')
    # if message.text == 'Редактировать группу':
    #     for group in groups:
    #         button = telebot.types.InlineKeyboardButton(text=group.name, callback_data='edit_' + group.name)
    #         markup.add(button)
    #     bot.send_message(message.chat.id, "Выбери группу которую хочешь отредактировать", reply_markup=markup)
    bot.send_message(message.chat.id, "send_to")

if __name__ == '__main__':
    bot.polling()