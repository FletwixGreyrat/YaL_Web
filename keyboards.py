from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def againkb(id):
    kb = InlineKeyboardMarkup()
    kb.insert(InlineKeyboardButton(text='Отправить еще одно сообщение🔁', callback_data=f'again:{id}'))
    return kb

def stopkb():
    kb = InlineKeyboardMarkup()
    kb.insert(InlineKeyboardButton(text='Отменить отправку💌', callback_data='otmenans'))
    return kb


def kb1(id):
    kb1 = InlineKeyboardMarkup()
    kb1.add(InlineKeyboardButton(text='Отменить отправку❌', callback_data=f'otmena:{id}'))
    return kb1


def answerkb(id):
    kb1 = InlineKeyboardMarkup()
    kb1.add(InlineKeyboardButton(text='Ответить💌', callback_data=f'a:{id}'))
    return kb1

def yesornokb():
    kb = InlineKeyboardMarkup()
    kb.insert(InlineKeyboardButton(text='Да', callback_data='yes'))
    kb.insert(InlineKeyboardButton(text="Нет", callback_data='no'))
    return kb


def yesorno1Kb():
    kb = InlineKeyboardMarkup()
    kb.insert(InlineKeyboardButton('Отправить', callback_data='send:a'))
    kb.insert(InlineKeyboardButton('Не отправлять', callback_data='send:b'))
    return kb


def basicKeyboard():
    pass