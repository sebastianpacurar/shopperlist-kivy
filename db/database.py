import os
import sqlite3
import mysql.connector
from decimal import Decimal
from decouple import config

from db.queries import QueriesSqlite, QueriesMysql

sqlite_db_path = os.path.join(os.getcwd(), '..', 'db', 'shopping_list_db.db')
SQLITE = 'sqlite'
MYSQL = 'mysql'


class Database:
    def __init__(self, rdbms):
        self.queries = None
        self.rdbms = rdbms

    def set_conn(self):
        match self.rdbms:
            case 'sqlite':
                self.queries = QueriesSqlite(self.rdbms)
                return sqlite3.connect(sqlite_db_path)
            case 'mysql':
                self.queries = QueriesMysql(self.rdbms)
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
            cursor.execute(self.queries.get_all_products())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_shop_lists(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_lists())
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get_product_categories(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_categories())
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get_product_units(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_product_units())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_shop_list(self, list_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_single_list(), (list_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def add_shopping_list(self, name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.insert_into_shopping_list(), (name,))
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
            cursor.execute(self.queries.get_category_id(), (category,))
            category_id = cursor.fetchone()[0]

            cursor.execute(self.queries.get_unit_id(), (unit,))
            unit_id = cursor.fetchone()[0]

            if self.rdbms == MYSQL:
                price = Decimal(price)

            cursor.execute(self.queries.insert_into_product(), (name, price, unit_id, category_id))
            conn.commit()
            return 1
        except Exception as e:
            conn.rollback()
            print(f'Exception when adding product: {e}')
            return 0
        finally:
            cursor.close()
            conn.close()
