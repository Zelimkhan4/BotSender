import telebot
import config
import pprint


bot = telebot.TeleBot(config.apikey)


@bot.message_handler(content_types=['text'])
def send_message(message):
    bot.send_message(message.chat.id, message.text)


bot.polling()