from .base_parser import BaseParser
from loader import db


class CategoryParser(BaseParser):
    def __init__(self, category):
        super().__init__(category)

    def get_data(self):
        data = []
        soup = self.get_soup()
        try:
            box = soup.find('div', class_='row-viewed col-catalog-grid product-grid')
            products = box.find_all('div', class_='col-lg-12 col-md-15 col-sm-20 col-xs-30 item-product')
            category_name = ''
            if self.category == 'kategory-noutbuki':
                category_name = 'Noutbuklar'
            elif self.category == 'kategory-klaviaturi':
                category_name = 'Klaviaturalar'
            elif self.category == 'kategory-mouses':
                category_name = 'Sichqonchalar'
            elif self.category == 'kategory-naushniki':
                category_name = 'Quloqchinlar'

            category_id = db.return_category_id(category_name)
            for item in products:
                title = item.find('a', class_='item-link').get_text(strip=True)
                image = 'https://upg.uz/' + item.find('a', class_='item-link').find('img')['src']
                link = item.find('a', class_='item-link')['href']
                price = int(item.find('span', class_='item-price price-new').get_text().replace(' ', '').replace('сум', ''))
                data.append({
                    'product_name': title,
                    'image': image,
                    'link': link,
                    'price': price,
                    'category_id': category_id
                })
            return data
        except:
            return "Noto'g'ri!!!"