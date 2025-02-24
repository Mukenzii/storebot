from bs4 import BeautifulSoup
import requests



class BaseParser:
    def __init__(self, category):
        self.category = category
        self.URL = 'https://upg.uz/ru/categories/'

    def get_soup(self):
        try:
            res = requests.get(self.URL + self.category).text
            soup = BeautifulSoup(res, 'html.parser')
            return soup
        except:
            return "Noto'g'ri ma'lumot kiritdingiz!"


class CategoryParser(BaseParser):
    def __init__(self, category):
        super().__init__(category)

    def get_data(self):
        data = []
        soup = self.get_soup()
        try:
            box = soup.find('div', class_='row-viewed col-catalog-grid product-grid')
            products = box.find_all('div', class_='col-lg-12 col-md-15 col-sm-20 col-xs-30 item-product')
            for item in products:
                title = item.find('a', class_='item-link').get_text(strip=True)
                image = 'https://upg.uz/' + item.find('a', class_='item-link').find('img')['src']
                link = item.find('a', class_='item-link')['href']
                price = int(item.find('span', class_='item-price price-new').get_text().replace(' ', '').replace('сум', ''))
                data.append({
                    'title': title,
                    'image': image,
                    'link': link,
                    'price': price
                })
            return data
        except:
            return "Noto'g'ri!!!"
