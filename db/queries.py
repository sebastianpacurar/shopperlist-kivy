class Queries:
    def get_all_products(self):
        return ' '.join('''
                SELECT 
                    product.product_id,
                    product.name,
                    category.name AS category_name 
                FROM product 
                JOIN category ON product.category_id = category.category_id
        '''.split())

    def get_all_lists(self):
        return ' '.join('''
                SELECT
                    shop_list.*,
                    user.name
                FROM shop_list
                INNER JOIN user ON shop_list.user_id = user.user_id
        '''.split())

    def get_all_categories(self):
        return 'SELECT * FROM category'

    def get_all_product_units(self):
        return 'SELECT * FROM product_unit'

    def check_if_any_user_active(self):
        return 'SELECT * FROM user WHERE online_status = 1'

    def get_all_lists_for_user(self):
        pass

    def get_single_list(self):
        pass

    def get_category_id(self):
        pass

    def get_unit_id(self):
        pass

    def insert_into_product(self):
        pass

    def insert_into_shopping_list(self):
        pass

    def create_user(self):
        pass

    def check_if_user_stored(self):
        pass

    def check_if_user_name_exists(self):
        pass

    def check_if_user_email_exists(self):
        pass

    def set_user_online_status(self):
        pass

    def unset_user_online_status(self):
        pass


class QueriesSqlite(Queries):
    _instance = None

    def __new__(cls, rdbms):
        if cls._instance is None or cls._instance.rdbms != rdbms:
            cls._instance = super().__new__(cls)
            cls._instance.rdbms = rdbms
        return cls._instance

    def get_all_products(self):
        return super().get_all_products()

    def get_all_lists(self):
        return super().get_all_lists()

    def get_all_categories(self):
        return super().get_all_categories()

    def get_all_product_units(self):
        return super().get_all_product_units()

    def check_if_any_user_active(self):
        return super().check_if_any_user_active()

    def get_all_lists_for_user(self):
        return 'SELECT * FROM shop_list WHERE user_id = ?'

    def get_single_list(self):
        return ' '.join('''
                SELECT
                    p.product_id,
                    p.name AS product_name,
                    p.price,
                    c.name AS category_name,
                    p.product_image,
                    slp.quantity AS quantity_in_list
                FROM shop_list_product AS slp
                JOIN product AS p ON slp.product_id = p.product_id
                LEFT JOIN category AS c ON p.category_id = c.category_id
                WHERE slp.shop_list_id = ?
                '''.split())

    def get_category_id(self):
        return 'SELECT category_id FROM category WHERE name = ?'

    def get_unit_id(self):
        return 'SELECT unit_id FROM product_unit WHERE name = ?'

    def insert_into_product(self):
        return 'INSERT INTO product (name, price, unit_id, category_id) VALUES (?, ?, ?, ?)'

    def insert_into_shopping_list(self):
        return 'INSERT INTO shop_list (name, user_id) VALUES (?, ?)'

    def check_if_user_stored(self):
        return 'SELECT * FROM user WHERE name = ? AND password = ?'

    def check_if_user_name_exists(self):
        return 'SELECT * FROM user WHERE name = ?'

    def check_if_user_email_exists(self):
        return 'SELECT * FROM user WHERE email = ?'

    def create_user(self):
        return 'INSERT INTO user (name, email, password, online_status) VALUES (?, ?, ?, 1)'

    def set_user_online_status(self):
        return 'UPDATE user SET online_status = 1 WHERE name= ?'

    def unset_user_online_status(self):
        return 'UPDATE user SET online_status = 0 WHERE name= ?'


class QueriesMysql(Queries):
    _instance = None

    def __new__(cls, rdbms):
        if cls._instance is None or cls._instance.rdbms != rdbms:
            cls._instance = super().__new__(cls)
            cls._instance.rdbms = rdbms
        return cls._instance

    def get_all_products(self):
        return super().get_all_products()

    def get_all_lists(self):
        return super().get_all_lists()

    def get_all_categories(self):
        return super().get_all_categories()

    def get_all_product_units(self):
        return super().get_all_product_units()

    def check_if_any_user_active(self):
        return super().check_if_any_user_active()

    def get_all_lists_for_user(self):
        return 'SELECT * FROM shop_list WHERE user_id = %s'

    def get_single_list(self):
        return ' '.join('''
                SELECT
                    p.product_id,
                    p.name AS product_name,
                    p.price,
                    c.name AS category_name,
                    p.product_image,
                    slp.quantity AS quantity_in_list
                FROM shop_list_product AS slp
                JOIN product AS p ON slp.product_id = p.product_id
                LEFT JOIN category AS c ON p.category_id = c.category_id
                WHERE slp.shop_list_id = %s
                '''.split())

    def get_category_id(self):
        return 'SELECT category_id FROM category WHERE name = %s'

    def get_unit_id(self):
        return 'SELECT unit_id FROM product_unit WHERE name = %s'

    def insert_into_product(self):
        return 'INSERT INTO product (name, price, unit_id, category_id) VALUES (%s, %s, %s, %s)'

    def insert_into_shopping_list(self):
        return 'INSERT INTO shop_list (name, user_id) VALUES (%s, %s)'

    def check_if_user_stored(self):
        return 'SELECT * FROM user WHERE name = %s AND password = %s'

    def check_if_user_name_exists(self):
        return 'SELECT * FROM user WHERE name = %s'

    def check_if_user_email_exists(self):
        return 'SELECT * FROM user WHERE email = %s'

    def create_user(self):
        return 'INSERT INTO user (name, email, password, online_status) VALUES (%s, %s, %s, 1)'

    def set_user_online_status(self):
        return 'UPDATE user SET online_status = 1 WHERE name= %s'

    def unset_user_online_status(self):
        return 'UPDATE user SET online_status = 0 WHERE name= %s'
