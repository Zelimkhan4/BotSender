from telebot import types


def generate_reply_markup(data):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=1)
    for but in data:
        markup.add(types.KeyboardButton(but))
    return markup
    
def generate_inline_markup(data):
    markup = types.InlineKeyboardMarkup()
    if len(data[0]) == 2:
        for but, call_data in data:
            markup.add(types.InlineKeyboardButton(but, callback_data=call_data))
        return markup


    for but in data:
        markup.add(types.InlineKeyboardButton(but))
    return markup

def generate_base_markup():
    functions = ["Имя и фамилия", "Роль", "Трек", "Всем"]
    callback_datas = ["Name", "Role", "Track", "All"]
    mark = types.InlineKeyboardMarkup()
    for i, f in  enumerate(functions):
        mark.add(types.InlineKeyboardButton(f, callback_data=callback_datas[i]))
    return mark