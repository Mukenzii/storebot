from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def register_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Ro'yxatdan o'tish ✍️"))
    return markup

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("Menyu 🛍"), KeyboardButton('Savat 🛒'),
        KeyboardButton('Sozlamalar ⚙️'), KeyboardButton('Aloqa 📲')
    )
    return markup

def send_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(KeyboardButton('Kontaktni ulashish', request_contact=True))
    return markup

def register_submit():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton('Ha'),
        KeyboardButton("Yo'q")
    )
    return markup

def categories_btn(category_list):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row_width = 2
    for i in category_list:
        markup.add(KeyboardButton(i[0]))
    markup.add('Asosiy Menyu')

    return markup


def admin_btn():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        KeyboardButton('Foydalanuchilar soni'),
        KeyboardButton('Foydalanuchilarga e\'lon'),
        KeyboardButton("Kategoriya qo'shish"),
        KeyboardButton("Kategoriyani o'chirish"),
        KeyboardButton("Product qo'shish"),
        KeyboardButton("Product o'chirish")
    )
    return markup

