from keyboards.default import main_menu
from keyboards.inline import card_items_btn



def get_card_text_markup(data: dict):
    text = "Savatda:\n"
    total_price = 0
    for product_name, items in data['card'].items():
        quantity, product_id, price = items['quantity'], items['product_id'], items['price']
        products_price = price * quantity
        total_price += products_price
        text += f"""\n{product_name}
Narxi: {price} * {quantity} = {products_price}\n"""
    if total_price == 0:
        text = "Savatingiz bo'sh!"
        markup = main_menu()
    else:
        text += f"\nUmumiy narx: {total_price}"
        markup = card_items_btn(data['card'])
    return {'markup': markup, 'text': text}