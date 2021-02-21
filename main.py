import telebot
import config
import pprint


bot = telebot.TeleBot(config.apikey)

class Group:
    def __init__(name, participants):
        self.name = name
        self.participants = participants

    def add_participant(participant):
        self.participants.append(participant)

@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.chat.id, message.text)


bot.polling()