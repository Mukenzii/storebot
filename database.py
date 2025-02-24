import psycopg2


class DataBase:
    def __init__(self, name, password, host, user):
        self.database = psycopg2.connect(
            database=name,
            password=password,
            host=host,
            user=user
        )

    def manager(self, sql, *args, commit: bool = False,
                fetchone: bool = False,
                fetchall: bool = False):
        with self.database as db:
            with db.cursor() as cursor:
                cursor.execute(sql, args)
                if commit:
                    return db.commit()
                elif fetchone:
                    return cursor.fetchone()
                elif fetchall:
                    return cursor.fetchall()

    def create_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(60),
            contact VARCHAR(20) UNIQUE,
            birthdate DATE
        )'''
        self.manager(sql, commit=True)

    def insert_users_tg(self, telegram_id):
        sql = '''INSERT INTO users(telegram_id) VALUES(%s)
                 ON CONFLICT DO NOTHING'''
        self.manager(sql, (telegram_id,), commit=True)

    def check_user_id(self, telegram_id):
        sql = '''SELECT * FROM users WHERE telegram_id = %s'''
        return self.manager(sql, telegram_id, fetchone=True)

    def save_user(self, full_name, contact, birthdate, telegram_id):
        sql = '''UPDATE users SET full_name=%s, contact=%s, birthdate=%s WHERE telegram_id=%s'''
        self.manager(sql, full_name, contact, birthdate, telegram_id)

    def create_categories(self):
        sql = '''CREATE TABLE IF NOT EXISTS categories(
            category_id SERIAL PRIMARY KEY,
            category VARCHAR(50) UNIQUE
        )'''
        self.manager(sql, commit=True)

    def create_products(self):
        sql = '''CREATE TABLE IF NOT EXISTS products(
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(150) UNIQUE,
            price INTEGER,
            image TEXT,
            link TEXT,
            category_id INTEGER REFERENCES categories(category_id) 
        )'''
        self.manager(sql, commit=True)

    def insert_category(self, category):
        sql = '''INSERT INTO categories(category) values (%s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, (category,), commit=True)

    def return_category_id(self, category):
        sql = '''SELECT category_id FROM categories WHERE category = %s'''
        return self.manager(sql, category, fetchone=True)[0]

    def insert_product(self, product_name, price, image, link, category_id):
        sql = '''INSERT INTO products(product_name, price, image, link, category_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING'''
        self.manager(sql, product_name, price, image, link, category_id, commit=True)

    def get_all_categories(self):
        sql = '''SELECT category FROM categories'''
        return self.manager(sql, fetchall=True)

    # def get_products_by_category(self, category):
    #     sql = '''SELECT * FROM products
    #     WHERE category_id=(SELECT category_id FROM categories WHERE category = %s)'''
    #     return self.manager(sql, category, fetchall=True)

    def get_products_by_category_pagination(self, category, offset, limit):
        sql = '''SELECT * FROM products
            WHERE category_id=(SELECT category_id FROM categories WHERE category = %s)
            OFFSET %s
            LIMIT %s'''
        return self.manager(sql, category, offset, limit, fetchall=True)

    def get_products_count(self, category):
        sql = '''SELECT count(product_id) FROM products 
        WHERE category_id=(SELECT category_id FROM categories WHERE category = %s)'''
        return self.manager(sql, category, fetchone=True)[0]

    def get_product_info(self, product_id):
        sql = '''SELECT * FROM products WHERE product_id=%s'''
        return self.manager(sql, product_id, fetchone=True)

    def get_category_by_id(self, category_id):
        sql = '''SELECT category FROM categories WHERE category_id=%s'''
        return self.manager(sql, category_id, fetchone=True)[0]

    def get_users_count(self):
        sql = '''SELECT count(telegram_id) FROM users'''
        return self.manager(sql, fetchone=True)[0]


    def get_users_id(self):
        sql = '''SELECT telegram_id FROM users'''
        return self.manager(sql, fetchall=True)

    def get_categories_for_del(self):
        sql = '''SELECT category, category_id FROM categories'''
        return self.manager(sql, fetchall=True)

    def delete_products_by_category(self, category_id):
        sql = '''DELETE FROM products WHERE category_id=%s'''
        self.manager(sql, category_id, commit=True)


    def delete_category(self, category_id):
        sql = '''DELETE FROM categories WHERE category_id=%s'''
        self.manager(sql, category_id, commit=True)

    def get_products_for_delete(self):
        sql = '''SELECT product_name, product_id FROM products'''
        return self.manager(sql, fetchall=True)

    def delete_product_by_id(self, product_id):
        sql = '''DELETE FROM products WHERE product_id=%s'''
        self.manager(sql, product_id, commit=True)

