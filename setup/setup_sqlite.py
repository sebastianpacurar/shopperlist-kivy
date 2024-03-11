import sqlite3
import os

from setup.add_img import insert_product_images
from db.database import get_sqlite_db_path


def get_sql_queries():
    sql_dir = os.path.join(os.getcwd(), 'sql')
    create_tables_file = os.path.join(sql_dir, 'sqlite3_tables.sql')
    insert_data_file = os.path.join(sql_dir, 'insert_data.sql')

    with open(create_tables_file, 'r') as file:
        create_tables = file.read()

    with open(insert_data_file, 'r') as file:
        insert_data = file.read()

    return f'{create_tables}\n{insert_data}'


if __name__ == '__main__':
    queries = get_sql_queries()
    conn = sqlite3.connect(get_sqlite_db_path())
    cursor = conn.cursor()
    cursor.executescript(queries)
    insert_product_images(conn)
