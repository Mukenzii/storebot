from telebot.types import CallbackQuery
from loader import bot, db

@bot.callback_query_handler(func=lambda call: 'del_category' in call.data)
def reaction_del_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    category_id = int(call.data.split('|')[1])
    print(category_id)
    db.delete_products_by_category(category_id)
    db.delete_category(category_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "O'chirildi!")


@bot.callback_query_handler(func=lambda call: 'del_product' in call.data)
def reaction_del_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    product_id = int(call.data.split('|')[1])
    db.delete_product_by_id(product_id)
    bot.send_message(chat_id, "O'chirildi!")


