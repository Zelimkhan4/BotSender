from telebot import types


def generate_markup(data):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=1)
    for i in data:
        markup.add(i[0])
    return markup


def generate_base_markup():
    functions = ["Просмотреть группу", "Редактировать группу", "Добавить группу", "Написать группе"]
    mark = types.ReplyKeyboardMarkup(one_time_keyboard=1)
    for f in functions:
        mark.add(f)
    return mark