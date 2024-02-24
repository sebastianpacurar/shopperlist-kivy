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
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_products())
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def get_product(self, product_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_product_details(), (product_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_all_shop_lists(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_lists())
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
            conn.close()

    def get_shop_lists_for_active_user(self, user_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_all_lists_for_user(), (user_id,))
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

    def filter_product_names(self, search_param):
        like_query = search_param + '%'
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.filter_product_based_on_name(), (like_query,))
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def get_active_user(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.check_if_any_user_active())
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def get_login_user(self, name, password):
        conn = self.set_conn()
        cursor = conn.cursor()
        user_data = {}
        try:
            cursor.execute(self.queries.check_if_user_stored(), (name, password))
            entry = cursor.fetchone()

            if entry:
                user_data = {
                    'id': entry[0],
                    'name': entry[1],
                    'email': entry[2]
                }
                try:
                    cursor.execute(self.queries.set_user_online_status(), (user_data['name'],))
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        return user_data

    def get_shop_list(self, list_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.get_single_list(), (list_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def user_logout(self, name):
        conn = self.set_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(self.queries.unset_user_online_status(), (name,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()

    def user_auto_login(self):
        conn = self.set_conn()
        cursor = conn.cursor()
        user_data = {}
        try:
            user = cursor.execute(self.queries.check_if_any_user_active()).fetchone()
            if user:
                user_data = {
                    'id': user[0],
                    'name': user[1],
                    'email': user[2]
                }
        finally:
            cursor.close()
            conn.close()
        return user_data

    def add_user(self, user, email, password):
        conn = self.set_conn()
        cursor = conn.cursor()
        user_data = {}
        try:
            check_one = cursor.execute(self.queries.check_if_user_email_exists(), (email,)).fetchone()
            check_two = cursor.execute(self.queries.check_if_user_name_exists(), (user,)).fetchone()
            if check_one or check_two:
                print('Error: User or email already exists')
            else:
                try:
                    cursor.execute(self.queries.create_user(), (user, email, password))
                    conn.commit()
                    user = cursor.execute(self.queries.check_if_user_stored(), (user, password)).fetchone()
                    user_data = {
                        'id': user[0],
                        'name': user[1],
                        'email': user[2]
                    }
                except Exception as e:
                    conn.rollback()
                    print(e)
        finally:
            cursor.close()
            conn.close()
        return user_data

    def add_shopping_list(self, name, user_id):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.insert_into_shopping_list(), (name, user_id))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
        return res

    def add_product(self, name, price, category, unit, img_path):
        conn = self.set_conn()
        cursor = conn.cursor()
        res = False
        try:
            cursor.execute(self.queries.get_category_id(), (category,))
            category_id = cursor.fetchone()[0]

            cursor.execute(self.queries.get_unit_id(), (unit,))
            unit_id = cursor.fetchone()[0]

            if self.rdbms == MYSQL:
                price = Decimal(price)

            cursor.execute(self.queries.insert_into_product(), (name, price, unit_id, category_id, img_path))
            conn.commit()
            res = True
        except Exception as e:
            conn.rollback()
            print(f'Exception when adding product: {e}')
        finally:
            cursor.close()
            conn.close()
        return res
