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
        return 'SELECT * FROM shop_list'

    def get_all_categories(self):
        return 'SELECT * FROM category'

    def get_all_product_units(self):
        return 'SELECT * FROM product_unit'

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
        return 'INSERT INTO shop_list (name) VALUES (?)'


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
        return 'INSERT INTO shop_list (name) VALUES (%s)'
