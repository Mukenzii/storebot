from telebot.types import Message, ReplyKeyboardRemove

from loader import bot, db
from config import ADMINS
from keyboards.default import admin_btn
from keyboards.inline import delete_category_btn, delete_product_btn
from states import ProductState


@bot.message_handler(chat_id=ADMINS, func=lambda message: message.text == 'Foydalanuchilar soni')
def reaction_users_count(message: Message):
    chat_id = message.chat.id
    users = db.get_users_count()
    bot.send_message(chat_id, f"Hozirda botni obunachilar soni: {users} ta")



@bot.message_handler(chat_id=ADMINS, func=lambda message: message.text == "Foydalanuchilarga e'lon")
def reaction_repost(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Jo'natish kerak bo'lgan ma'lumotni kiriting",
                     reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, repost)


def repost(message: Message):
    chat_id = message.chat.id
    users = db.get_users_id()
    count_users = db.get_users_count()
    iterator = 0
    error = 0
    try:
        for user in users:
            bot.copy_message(user[0], chat_id, message.id)
            iterator += 1
    except:
        error += 1

    for admin in ADMINS:
        bot.send_message(admin, f"""Jo'natildi {iterator}/{count_users},
Muammolar bo'ldi: {error}""", reply_markup=admin_btn())


@bot.message_handler(chat_id=ADMINS, func=lambda message: message.text == "Kategoriya qo'shish")
def reaction_add_category(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Kategoriya nomini kiriting", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, add_category)


def add_category(message: Message):
    chat_id = message.chat.id
    category = message.text.capitalize()
    db.insert_category(category)
    bot.send_message(chat_id, "Qo'shildi!", reply_markup=admin_btn())


@bot.message_handler(chat_id=ADMINS, func=lambda message: message.text == "Product qo'shish")
def reaction_add_product(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.set_state(user_id, ProductState.product_name, chat_id)
    bot.send_message(chat_id, "Product nomini kiriting", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(chat_id=ADMINS, content_types=['text'], state=ProductState.product_name)
def product_name(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['product_name'] = message.text.capitalize()
    bot.set_state(user_id, ProductState.price, chat_id)
    bot.send_message(chat_id, "Product narxini kiriting", reply_markup=ReplyKeyboardRemove())


@bot.message_handler(chat_id=ADMINS, content_types=['text'], state=ProductState.price)
def product_price(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['price'] = message.text.capitalize()
    bot.set_state(user_id, ProductState.image, chat_id)
    bot.send_message(chat_id, "Product rasmini havolasini kiriting",
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(chat_id=ADMINS, content_types=['text'], state=ProductState.image)
def product_image(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['image'] = message.text
    bot.set_state(user_id, ProductState.link, chat_id)
    bot.send_message(chat_id, "Product havolasini kiriting",
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(chat_id=ADMINS, content_types=['text'], state=ProductState.link)
def product_link(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        data['link'] = message.text
    bot.set_state(user_id, ProductState.category, chat_id)
    bot.send_message(chat_id, "Product categoriyasini kiriting",
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(chat_id=ADMINS, content_types=['text'], state=ProductState.category)
def product_category(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        product_name = data['product_name']
        price = data['price']
        image = data['image']
        link = data['link']
        category = message.text.capitalize()
    category_id = db.return_category_id(category)
    db.insert_product(product_name, price, image, link, category_id)
    bot.delete_state(user_id, chat_id)
    bot.send_message(chat_id, "Product kiritildi!",
                     reply_markup=admin_btn())

@bot.message_handler(chat_id=ADMINS, func=lambda message: message.text == "Kategoriyani o'chirish")
def reaction_delete_category(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Kategoriyani tanlang!",
                     reply_markup=delete_category_btn(db.get_categories_for_del()))

@bot.message_handler(chat_id=ADMINS, func=lambda message: message.text == "Product o'chirish")
def reaction_delete_product(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Productni tanlang!",
                     reply_markup=delete_product_btn(db.get_products_for_delete()))




