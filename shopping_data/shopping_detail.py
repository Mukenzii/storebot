from telebot.types import LabeledPrice
from .shop_product import Product


def generate_product_invoice(product_data):
    query = Product(
        title='Shop BOT',
        description='\n'.join([title for title in product_data]),
        currency='UZS',
        prices=[LabeledPrice(label=f"{product_data[title]['quantity']} {title}",
        amount=int(product_data[title]['quantity']) * int(product_data[title]['price']) * 100)
                for title in product_data],
        start_parameter='create_invoice_products',
        need_name=True,
        need_phone_number=True,
        is_flexible=True
    )
    return query

