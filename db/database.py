import os
import sqlite3
from decimal import Decimal

import mysql.connector
from decouple import config

sqlite_db_path = os.path.join(os.getcwd(), 'shopping_list_db.db')
SQLITE = 'sqlite'
MYSQL = 'mysql'


class Database:
    def __init__(self, rdbms):
        self.sub = ''
        self.rdbms = rdbms
        self.tables = []
        self.curr_table = None

    def set_conn(self):
        match self.rdbms:
            case 'sqlite':
                self.sub = '?'
                return sqlite3.connect(sqlite_db_path)
            case 'mysql':
                self.sub = '%s'
                return mysql.connector.connect(
                    host=config('DB_HOST'),
                    user=config('DB_USER'),
                    password=config('DB_PASSWORD'),
                    database='shopping_list_db'
                )

    def get_all_products(self):
        """ get all columns of a table """
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"SELECT product.product_id, product.name, category.name AS category_name FROM product JOIN category ON product.category_id = category.category_id")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_shop_lists(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM shop_list")
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get_product_categories(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM category")
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get_product_units(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM product_unit")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_shop_list(self, list_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(
                ' '.join(f'''
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
                        slp.shop_list_id = {self.sub};
                '''.split()), (list_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def add_shopping_list(self, name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(f"INSERT INTO shop_list (name) VALUES ({self.sub})", (name,))
            conn.commit()
            return 1
        except Exception as e:
            conn.rollback()
            return 0
        finally:
            cursor.close()
            conn.close()

    def add_product(self, name, price, category, unit):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT category_id FROM category WHERE name = {self.sub}", (category,))
            category_id = cursor.fetchone()[0]

            cursor.execute(f"SELECT unit_id FROM product_unit WHERE name = {self.sub}", (unit,))
            unit_id = cursor.fetchone()[0]

            if self.rdbms == MYSQL:
                price = Decimal(price)

            cursor.execute(
                f"INSERT INTO product (name, price, unit_id, category_id) VALUES ({self.sub}, {self.sub}, {self.sub}, {self.sub})",
                (name, price, unit_id, category_id))
            conn.commit()
            return 1
        except Exception as e:
            conn.rollback()
            print(f'Exception when adding product: {e}')
            return 0
        finally:
            cursor.close()
            conn.close()
