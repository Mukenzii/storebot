from telebot.types import CallbackQuery

from handlers.users.utils import get_card_text_markup
from loader import bot, db

from keyboards.default import *
from keyboards.inline import *
from states import CardState

from shopping_data.shopping_detail import generate_product_invoice


@bot.callback_query_handler(func=lambda call: call.data == 'next')
def reaction_next(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards_list = call.message.reply_markup.keyboard[-2]
    for btn in keyboards_list:
        if 'page' in btn.callback_data:
            page = int(btn.text)
            category = btn.callback_data.split('|')[1]
            page += 1
            bot.edit_message_reply_markup(chat_id, call.message.id,
                                          reply_markup=products_btn_pagination(category, page))

@bot.callback_query_handler(func=lambda call: call.data == 'preview')
def reaction_preview(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards_list = call.message.reply_markup.keyboard[-2]
    for btn in keyboards_list:
        if 'page' in btn.callback_data:
            page = int(btn.text)
            category = btn.callback_data.split('|')[1]
            page -= 1
            bot.edit_message_reply_markup(chat_id, call.message.id,
                                          reply_markup=products_btn_pagination(category, page))

@bot.callback_query_handler(func=lambda call: call.data == 'back_categories')
def reaction_back_categories(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "Kategoriyalar", reply_markup=categories_btn(db.get_all_categories()))

@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def reaction_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, 'Asosiy menyu', reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: 'page' in call.data)
def reaction_page(call: CallbackQuery):
    keyboards_list = call.message.reply_markup.keyboard[-2]
    for btn in keyboards_list:
        if 'page' in btn.callback_data:
            page = int(btn.text)
            bot.answer_callback_query(call.id, f"{page}chi betdasiz!")

@bot.callback_query_handler(func=lambda call: 'product' in call.data)
def reaction_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards_list = call.message.reply_markup.keyboard[-2]
    page = 1
    for btn in keyboards_list:
        if 'page' in btn.callback_data:
            page = int(btn.text)
    product_id = int(call.data.split('|')[1])
    product = db.get_product_info(product_id)
    product_name, price, image, link, category_id = product[1:]
    bot.delete_message(chat_id, call.message.id)
    bot.send_photo(chat_id, image, caption=f'''{product_name}
Narxi: <b>{price}</b>
<a href='{link}'>Batafsil ma'lumot</a>''', parse_mode="HTML",
                   reply_markup=product_items_btn(category_id, page, product_id))


@bot.callback_query_handler(func=lambda call: call.data == 'plus')
def reaction_plus(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards_list = call.message.reply_markup.keyboard
    product_id = int(keyboards_list[1][0].callback_data.split('|')[1])
    category_id = int(keyboards_list[-1][0].callback_data.split('|')[1])
    page = int(keyboards_list[0][1].callback_data.split('|')[1])
    quantity = int(keyboards_list[0][1].text)
    quantity += 1
    bot.edit_message_reply_markup(chat_id, call.message.id,
                reply_markup=product_items_btn(category_id, page, product_id, quantity))


@bot.callback_query_handler(func=lambda call: call.data == 'minus')
def reaction_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    keyboards_list = call.message.reply_markup.keyboard
    product_id = int(keyboards_list[1][0].callback_data.split('|')[1])
    category_id = int(keyboards_list[-1][0].callback_data.split('|')[1])
    page = int(keyboards_list[0][1].callback_data.split('|')[1])
    quantity = int(keyboards_list[0][1].text)
    if quantity > 1:
        quantity -= 1
        bot.edit_message_reply_markup(chat_id, call.message.id,
                reply_markup=product_items_btn(category_id, page, product_id, quantity))
    else:
        bot.answer_callback_query(call.id, "Kamida 1ta mahsulot bo'lishi shart⚠️", show_alert=True)


@bot.callback_query_handler(func=lambda call: 'back_cat_id' in call.data)
def reaction_back_by_category_id(call: CallbackQuery):
    chat_id = call.message.chat.id
    page = int(call.message.reply_markup.keyboard[0][1].callback_data.split('|')[1])
    category_id = int(call.data.split('|')[1])
    category = db.get_category_by_id(category_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, category, reply_markup=products_btn_pagination(category, page))



@bot.callback_query_handler(func=lambda call: 'add_card' in call.data)
def reaction_add_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.set_state(user_id, CardState.card, chat_id)
    product_id = int(call.data.split('|')[1])
    product = db.get_product_info(product_id)
    product_name, price = product[1:3]
    quantity = int(call.message.reply_markup.keyboard[0][1].text)

    with bot.retrieve_data(user_id, chat_id) as data:
        if data.get('card'):
            data['card'][product_name] = {
                'quantity': quantity,
                'product_id': product_id,
                'price': price
            }
        else:
            data['card'] = {
                product_name:{
                    'quantity': quantity,
                    'product_id': product_id,
                    'price': price
                }
            }
    bot.answer_callback_query(call.id, "Qo'shildi!")

@bot.callback_query_handler(func=lambda call: call.data == 'show_card')
def reaction_show_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        res = get_card_text_markup(data)
        text, markup = res['text'], res['markup']
        bot.delete_message(chat_id, call.message.id)
        bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: 'remove' in call.data)
def reaction_remove(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    product_id = int(call.data.split('|')[1])
    with bot.retrieve_data(user_id, chat_id) as data:
        keys = [product_name for product_name in data['card'].keys()]
        for item in keys:
            if data['card'][item]['product_id'] == product_id:
                del data['card'][item]

    res = get_card_text_markup(data)
    text, markup = res['text'], res['markup']
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'clear_card')
def reaction_clear_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    bot.delete_state(user_id, chat_id)
    bot.delete_message(chat_id, call.message.id)
    bot.send_message(chat_id, "Savat bo'sh!", reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: call.data == 'submit')
def reaction_submit_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    with bot.retrieve_data(user_id, chat_id) as data:
        bot.send_invoice(chat_id, **generate_product_invoice(data['card']).generate_invoice(),
                         invoice_payload='shop_bot')





