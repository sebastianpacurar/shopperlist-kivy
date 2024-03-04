class Queries:
    def get_all_products(self):
        return ' '.join('''
                SELECT 
                    product.product_id,
                    product.name,
                    category.name,
                    product.product_image
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

    def set_list_name(self):
        pass

    def delete_list(self):
        pass

    def get_category_id(self):
        pass

    def get_all_products_of_category_type(self):
        pass

    def insert_into_category(self):
        pass

    def set_category_name(self):
        pass

    def delete_category(self):
        pass

    def get_unit_id(self):
        pass

    def get_all_products_of_unit_type(self):
        pass

    def insert_into_unit(self):
        pass

    def set_unit_name(self):
        pass

    def delete_unit(self):
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

    def filter_product_based_on_name(self):
        pass

    def filter_category(self):
        pass

    def filter_unit(self):
        pass

    def get_product_details(self):
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

    def set_list_name(self):
        return 'UPDATE shop_list SET name = ? WHERE shop_list_id= ?'

    def delete_list(self):
        return 'DELETE FROM shop_list WHERE shop_list_id = ?'

    def get_category_id(self):
        return 'SELECT category_id FROM category WHERE name = ?'

    def get_all_products_of_category_type(self):
        return ' '.join('''
                SELECT 
                    product.product_id,
                    product.name,
                    category.category_id,
                    category.name,
                    product.product_image
                FROM product 
                JOIN category ON product.category_id = category.category_id
                WHERE category.category_id = ?
        '''.split())

    def insert_into_category(self):
        return 'INSERT INTO category (name) VALUES (?)'

    def set_category_name(self):
        return 'UPDATE category SET name = ? WHERE category_id = ?'

    def delete_category(self):
        return 'DELETE FROM category WHERE category_id = ?'

    def get_unit_id(self):
        return 'SELECT unit_id FROM product_unit WHERE name = ?'

    def get_all_products_of_unit_type(self):
        return ' '.join('''
                SELECT 
                    product.product_id,
                    product.name,
                    product_unit.unit_id,
                    product_unit.name,
                    product.product_image
                FROM product 
                JOIN product_unit ON product.unit_id = product_unit.unit_id
                WHERE product_unit.unit_id = ?
        '''.split())

    def insert_into_unit(self):
        return 'INSERT INTO product_unit (name) VALUES (?)'

    def set_unit_name(self):
        return 'UPDATE product_unit SET name = ? WHERE unit_id = ?'

    def delete_unit(self):
        return 'DELETE FROM product_unit WHERE unit_id = ?'

    def insert_into_product(self):
        return 'INSERT INTO product (name, price, unit_id, category_id, product_image) VALUES (?, ?, ?, ?, ?)'

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

    def filter_product_based_on_name(self):
        return ' '.join('''
                SELECT
                    product.product_id,
                    product.name,
                    category.name,
                    product.product_image
                FROM product
                JOIN category ON product.category_id = category.category_id
                WHERE product.name LIKE ?;
        '''.split())

    def filter_category(self):
        return 'SELECT * FROM category WHERE name LIKE ?'

    def filter_unit(self):
        return 'SELECT * FROM product_unit WHERE name LIKE ?'

    def get_product_details(self):
        return ' '.join('''
                SELECT 
                    product.product_id,
                    product.name,
                    category.name,
                    product_unit.name,
                    product.price,
                    product.product_image
                FROM 
                    product
                JOIN 
                    category ON product.category_id = category.category_id
                JOIN 
                    product_unit ON product.unit_id = product_unit.unit_id
                WHERE 
                    product.product_id = ?        
        '''.split())


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

    def set_list_name(self):
        return 'UPDATE shop_list SET name = %s WHERE shop_list_id= %s'

    def delete_list(self):
        return 'DELETE FROM shop_list WHERE shop_list_id = %s'

    def get_category_id(self):
        return 'SELECT category_id FROM category WHERE name = %s'

    def get_all_products_of_category_type(self):
        return ' '.join('''
                SELECT 
                    product.product_id,
                    product.name,
                    category.category_id,
                    category.name,
                    product.product_image
                FROM product 
                JOIN category ON product.category_id = category.category_id
                WHERE category.category_id = %s
        '''.split())

    def insert_into_category(self):
        return 'INSERT INTO category (name) VALUES (%s)'

    def set_category_name(self):
        return 'UPDATE category SET name = %s WHERE category_id = %s'

    def delete_category(self):
        return 'DELETE FROM category WHERE category_id = %s'

    def get_unit_id(self):
        return 'SELECT unit_id FROM product_unit WHERE name = %s'

    def get_all_products_of_unit_type(self):
        return ' '.join('''
                SELECT 
                    product.product_id,
                    product.name,
                    product_unit.unit_id,
                    product_unit.name,
                    product.product_image
                FROM product 
                JOIN product_unit ON product.unit_id = product_unit.unit_id
                WHERE product_unit.unit_id = %s
        '''.split())

    def insert_into_unit(self):
        return 'INSERT INTO product_unit (name) VALUES (%s)'

    def set_unit_name(self):
        return 'UPDATE product_unit SET name = %s WHERE unit_id = %s'

    def delete_unit(self):
        return 'DELETE FROM product_unit WHERE unit_id = %s'

    def insert_into_product(self):
        return 'INSERT INTO product (name, price, unit_id, category_id, product_image) VALUES (%s, %s, %s, %s, %s)'

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

    def filter_product_based_on_name(self):
        return ' '.join('''
                SELECT
                    product.product_id,
                    product.name,
                    category.name,
                    product.product_image
                FROM product
                JOIN category ON product.category_id = category.category_id
                WHERE product.name LIKE %s;
        '''.split())

    def filter_category(self):
        return 'SELECT * FROM category WHERE name LIKE %s'

    def filter_unit(self):
        return 'SELECT * FROM product_unit WHERE name LIKE %s'

    def get_product_details(self):
        return ' '.join('''
                SELECT 
                    product.product_id,
                    product.name,
                    category.name,
                    product_unit.name,
                    product.price,
                    product.product_image
                FROM 
                    product
                JOIN 
                    category ON product.category_id = category.category_id
                JOIN 
                    product_unit ON product.unit_id = product_unit.unit_id
                WHERE 
                    product.product_id = %s        
        '''.split())
