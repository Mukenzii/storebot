from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import db


# def products_btn(product_list):
#     markup = InlineKeyboardMarkup()
#     for item in product_list:
#         markup.add(InlineKeyboardButton(item[1], callback_data=f'product|{item[0]}'))
#     return markup

def products_btn_pagination(category, page=1):
    markup = InlineKeyboardMarkup(row_width=1)
    limit = 5
    offset = (page - 1) * limit
    count = db.get_products_count(category)
    max_page = count // limit if count % limit == 0 else count // limit + 1
    products = db.get_products_by_category_pagination(category, offset, limit)
    for item in products:
        markup.add(InlineKeyboardButton(item[1], callback_data=f"product|{item[0]}"))

    preview_btn = InlineKeyboardButton('◀️', callback_data='preview')
    page_btn = InlineKeyboardButton(page, callback_data=f'page|{category}')
    next_btn = InlineKeyboardButton('▶️', callback_data='next')

    if page == 1:
        markup.row(page_btn, next_btn)
    elif 1 < page < max_page:
        markup.row(preview_btn, page_btn, next_btn)
    elif page == max_page:
        markup.row(preview_btn, page_btn)

    back = InlineKeyboardButton("🔙 Ortga", callback_data='back_categories')
    main_menu = InlineKeyboardButton('Asosiy menyu', callback_data='main_menu')
    markup.row(back, main_menu)

    return markup

def product_items_btn(category_id, page, product_id, quantity=1):
    items = [
        InlineKeyboardButton('➖', callback_data='minus'),
        InlineKeyboardButton(quantity, callback_data=f'quantity|{page}'),
        InlineKeyboardButton('➕', callback_data='plus')
    ]

    add_card = InlineKeyboardButton('Savatga qo\'shish', callback_data=f'add_card|{product_id}')
    card = InlineKeyboardButton('Savat 🛒', callback_data='show_card')
    back = InlineKeyboardButton('🔙 Ortga', callback_data=f"back_cat_id|{category_id}")
    main_menu = InlineKeyboardButton('Asosiy menyu', callback_data='main_menu')

    return InlineKeyboardMarkup(keyboard=[
        items,
        [add_card, card],
        [back, main_menu]
    ])


def card_items_btn(data: dict):
    markup = InlineKeyboardMarkup(row_width=1)
    for product_name, items in data.items():
        product_id = items['product_id']
        markup.add(InlineKeyboardButton(f"❌ {product_name}", callback_data=f"remove|{product_id}"))
    markup.row(
        InlineKeyboardButton('🔄 Tozalash', callback_data='clear_card'),
        InlineKeyboardButton('✅ Tasdiqlash', callback_data='submit')
    )
    markup.add(InlineKeyboardButton('Kategoriyalar', callback_data='back_categories'))
    return markup


def delete_category_btn(category_list):
    markup = InlineKeyboardMarkup(row_width=1)
    for item in category_list:
        markup.add(InlineKeyboardButton(item[0], callback_data=f"del_category|{item[1]}"))
    return markup

def delete_product_btn(product_list):
    markup = InlineKeyboardMarkup(row_width=1)
    for item in product_list:
        markup.add(InlineKeyboardButton(item[0], callback_data=f"del_product|{item[1]}"))
    return markup


