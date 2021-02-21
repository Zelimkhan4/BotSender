import telebot
import config
import pprint
import random


bot = telebot.TeleBot(config.apikey)


groups = []


class Group:
    def __init__(self, name, participants):
        self.name = name
        self.participants = participants
        print(self.participants)

    def add_participant(self, participant):
        self.participants.append(participant)
    
    def get_info(self):
        return "\n".join(i.get_info() for i in self.participants)



class Contact:
    def __init__(self, name, options):
        self.number = options['number']
        self.name = name
        self.profession = options['profession']
        self.rank = options['rank']
        self.track = options['track']
        self.old = options['old']
        self.ed_place = options['ed_place']

    def get_info(self):
        return f"""Contact name: {self.name}\n    number: {self.number}\n    Profession: {self.profession}\n    Rank: {self.rank}\n    Ed. place: {self.ed_place}\n    Old: {self.old}\n    Track: {self.track}"""


names = {'Zelimkhan': {'number':'89991429243',
                         'profession': 'Programmer',
                         'rank': 0,
                         'track': 'Innovator', 
                         'ed_place': 'shkola',
                         'old': 3000},
        'Aishat': {'number': '89282690871',
                         'profession': 'Designer',
                         'rank': 2,
                         'track': 'Activist',
                         'ed_place': 'shkola',
                         'old': 22},
        'Samad': {'number': '89626564991',
                         'profession': 'Unreal Dev',
                         'rank': 4,
                         'track': 'Innovator',
                         'ed_place': 'shkola',
                         "old": 16},
        "Deni": {'number': '89383526230',
                         'profession': 'Project Manager',
                         'rank': 4,
                         'track': 'Proektirovshik', 
                         'old': 21,
                         'ed_place': 'shkola'}}


participants = [Contact(name, names[name]) for name in names]
all_residents = Group("All", participants)


innovatorsh = Group('Innovators', participants)


groups.append(all_residents)
groups.append(innovatorsh)


status_of_printing_info = True
markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(telebot.types.KeyboardButton('Просмотреть все группы.', ))
markup.add(telebot.types.KeyboardButton('Добавить группу.'))
markup.add(telebot.types.KeyboardButton('Редактировать группу.'))
current_group = None

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'''Здравствуй {message.from_user.first_name}.\n
Я бот для рассылки сообщений.''', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def send_message(message):
    global current_group
    global status_of_printing_info
    if message.text == 'Просмотреть все группы.':
        for group in groups:
            bot.send_message(message.chat.id, f"Group name: {group.name}")
            bot.send_message(message.chat.id, group.get_info())



bot.polling()