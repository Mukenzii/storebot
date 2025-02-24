from loader import db, bot
from middlewares import SimpleMiddleware
from parser_file.parser_run import CategoryParser

# db.create_users()
# db.create_categories()
# db.create_products()
#
# categories = ['Noutbuklar', 'Klaviaturalar', 'Sichqonchalar', 'Quloqchinlar']
# for i in categories:
#     db.insert_category(i)
#
# product_list = ['kategory-noutbuki', 'kategory-klaviaturi', 'kategory-mouses', 'kategory-naushniki']
# products = [CategoryParser(i).get_data() for i in product_list]
# for item in products:
#     for product in item:
#         db.insert_product(**product)

import handlers


bot.setup_middleware(SimpleMiddleware(0.6))
if __name__ == '__main__':
    print('Bot ishladi...')
    bot.infinity_polling()
