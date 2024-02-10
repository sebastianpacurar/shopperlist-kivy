from decouple import config
import mysql.connector


class Database:
    def __init__(self):
        self.tables = []
        self.curr_table = None
        self.host = config('DB_HOST')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')

        self.init_app_start()

    def set_conn(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database='shopping_list_db'
        )

    def get_all_tables(self):
        """ get all tables from current db """
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            parsed = [x[0] for x in cursor.fetchall()]
            return parsed

    def get_all_products(self):
        """ get all columns of a table """
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT product.product_id, product.name, category.name AS category_name FROM product JOIN category ON product.category_id = category.category_id")
            return cursor.fetchall()

    def get_shop_lists(self):
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute("Select * From  shop_list")
            return cursor.fetchall()

    def get_product_categories(self):
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM category")
            return cursor.fetchall()

    def get_product_units(self):
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM product_unit")
            return cursor.fetchall()

    def get_shop_list(self, list_id):
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute(
                ' '.join('''
                    SELECT
                        p.product_id,
                        p.name AS product_name,
                        p.price,
                        c.name AS category_name,
                        p.product_image,
                        slp.quantity AS quantity_in_list
                    FROM
                        shop_list_product AS slp
                    JOIN
                        product AS p ON slp.product_id = p.product_id
                    LEFT JOIN
                        category AS c ON p.category_id = c.category_id
                    WHERE
                        slp.shop_list_id = %s;
                '''.split()), (list_id,))
            return cursor.fetchall()

    def get_table_cols_list(self):
        """ get all table columns as list"""
        conn = self.set_conn()
        with conn.cursor() as cursor:
            cursor.execute(f"SHOW COLUMNS FROM {self.curr_table}")
            return cursor.fetchall()

    def add_shopping_list(self, name):
        conn = self.set_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO shop_list (name) VALUES (%s)", (name,))
                conn.commit()
                return 1
        except Exception as e:
            conn.rollback()
            return 0
        finally:
            conn.close()

    def add_product(self, name, price, category, unit):
        conn = self.set_conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT category_id FROM category WHERE name = %s", (category,))
                category_id = cursor.fetchone()[0]

                cursor.execute("SELECT unit_id FROM product_unit WHERE name = %s", (unit,))
                unit_id = cursor.fetchone()[0]

                cursor.execute("INSERT INTO product (name, price, category_id, unit) VALUES (%s, %s, %s, %s)",
                               (name, price, category_id, unit_id))
                conn.commit()
                return 1
        except Exception as e:
            conn.rollback()
            return 0
        finally:
            conn.close()

    def set_table(self, target):
        self.curr_table = target

    def set_tables(self):
        self.tables = self.get_all_tables()
        self.set_table(self.tables[0])

    def init_app_start(self):
        self.curr_table = self.get_all_tables()[0]
