from telebot.types import Message, ReplyKeyboardRemove
import re

from loader import bot, db
from keyboards.default import *
from keyboards.inline import *
from states import RegisterStates


@bot.message_handler(func=lambda message: message.text == 'Menyu 🛍', chat_types='private')
def reaction_menu(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    check = db.check_user_id(user_id)
    if None in check:
        text = "Siz ro'yxatdan o'tmagansiz!\nIltimos buyurtma berish uchun ro'yxatdan o'ting😊"
        markup = register_btn()
    else:
        text = "Menyu"
        markup = categories_btn(db.get_all_categories())
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan o'tish ✍️")
def reaction_register(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, RegisterStates.full_name, chat_id)
    bot.send_message(chat_id, "Ism familiyangizni kiriting", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'], state=RegisterStates.full_name)
def reaction_full_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if ' ' in message.text:
            data['full_name'] = ' '.join([item.capitalize() for item in message.text.split(' ')])
        else:
            data['full_name'] = message.text.capitalize()

    bot.set_state(user_id, RegisterStates.contact, chat_id)
    bot.send_message(chat_id, 'Kontaktingizni kiriting', reply_markup=send_contact())


@bot.message_handler(content_types=['text', 'contact'], state=RegisterStates.contact)
def reaction_contact(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if message.contact:
            data['contact'] = message.contact.phone_number
            bot.set_state(user_id, RegisterStates.birthdate, chat_id)
            bot.send_message(chat_id, "Tug'ilgan kuningizni kiriting",
                             reply_markup=ReplyKeyboardRemove())
        else:

            if ' ' in message.text and '-' in message.text:
                number = message.text.replace(' ', '')
                number = number.replace('-', '')
            elif '-' in message.text:
                number = message.text.replace('-', '')
            elif ' ' in message.text:
                number = message.text.replace(' ', '')
            else:
                number = message.text

            if re.match(r"^(\+998)?(88|33|9(3|4|7|0|9))\d{7}$", number):
                data['contact'] = number
                bot.set_state(user_id, RegisterStates.birthdate, chat_id)
                bot.send_message(chat_id, "Tug'ilgan kuningizni kiriting: dd.mm.yyyy",
                                 reply_markup=ReplyKeyboardRemove())
            else:
                bot.set_state(user_id, RegisterStates.contact, chat_id)
                bot.send_message(chat_id, "Kontakt noto'g'ri boshidan kiriting!", reply_markup=send_contact())


@bot.message_handler(content_types=['text'], state=RegisterStates.birthdate)
def reaction_birthdate(message: Message):
    chat_id = message.chat.id
    user_id = message.chat.id
    with bot.retrieve_data(user_id, chat_id) as data:
        if re.match(
                r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})",
                message.text):
            data['birthdate'] = '.'.join(message.text.split('.')[::-1])
            name = data['full_name']
            contact = data['contact']
            bot.set_state(user_id, RegisterStates.submit, chat_id)
            bot.send_message(chat_id, f"""Tekshirib oling:

<b>Ism familiya: {name}</b>
<b>Kontakt: {contact}</b>
<b>tug'ilgan kun: {message.text}</b>

Ma'lumotlar to'g'rimi?""", reply_markup=register_submit(), parse_mode='HTML')
        else:
            bot.set_state(user_id, RegisterStates.birthdate, chat_id)
            bot.send_message(chat_id, "Qaytadan tug'ilgan kuningizni kiriting: dd.mm.yyyy")


@bot.message_handler(content_types=['text'], state=RegisterStates.submit)
def reaction_submit(message: Message):
    chat_id = message.chat.id
    user_id = message.chat.id
    if message.text == 'Ha':
        with bot.retrieve_data(user_id, chat_id) as data:
            name = data['full_name']
            contact = data['contact']
            birthdate = '.'.join(data['birthdate'].split('.')[::-1])
            db.save_user(name, contact, birthdate, user_id)
            bot.send_message(chat_id, "Saqlandi!", reply_markup=categories_btn(db.get_all_categories()))
        bot.delete_state(user_id, chat_id)
    else:
        bot.delete_state(user_id, chat_id)
        bot.set_state(user_id, RegisterStates.full_name, chat_id)
        bot.send_message(chat_id, "Ism familiyangizni qaytadan kiriting!",
                         reply_markup=ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: message.text == 'Asosiy Menyu')
def reaction_main_menu(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Asosiy Menyu", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text in [item[0] for item in db.get_all_categories()])
def reaction_categories(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "⏳", reply_markup=ReplyKeyboardRemove())
    bot.delete_message(chat_id, message.id + 1)
    bot.send_message(chat_id, message.text, reply_markup=products_btn_pagination(message.text))




