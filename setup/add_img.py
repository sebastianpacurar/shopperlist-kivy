import os
import sqlite3
import mysql.connector
from decouple import config

try:
    mysql_conn = mysql.connector.connect(
        host=config('DB_HOST'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        database='shopping_list_db'
    )
    print("MySQL connection selected")
except Exception as e:
    print("MySQL is not selected or connection failed")


def insert_product_images(conn):
    curr_dir = os.path.dirname(__file__)
    parent_dir = os.path.abspath(os.path.join(curr_dir, os.pardir))
    path = os.path.normpath(os.path.relpath(os.path.join('..', parent_dir, "png")))
    sub = '?' if isinstance(conn, sqlite3.Connection) else '%s'

    product_images = {
        "Smartphone": "smartphone.png",
        "Laptop": "laptop.png",
        "T-shirt": "t-shirt.png",
        "Jeans": "jeans.png",
        "Milk": "milk.png",
        "Sofa": "sofa.png",
        "Shampoo": "shampoo.png",
        "Toothpaste": "toothpaste.png",
        "Headphones": "headphones.png",
        "Running Shoes": "running shoes.png",
        "Coffee": "coffee.png",
        "Chocolate": "chocolate.png"
    }

    cursor = conn.cursor()
    for product_name, image_filename in product_images.items():
        img_path = os.path.join(path, image_filename)
        cursor.execute(f"SELECT product_image FROM product WHERE name = {sub}", (product_name,))
        curr_val = cursor.fetchone()[0]

        if curr_val is None:
            update_query = f"UPDATE product SET product_image = {sub} WHERE name = {sub}"
            cursor.execute(update_query, (img_path, product_name))
            print(f'UPDATED - Product {product_name} contains {img_path}')
        else:
            print(f'SKIPPED - Product {product_name} already contains {curr_val}')

    conn.commit()
    conn.close()


# Being held for testing purposes - used to populate mysql product images directly
if __name__ == '__main__':
    insert_product_images(mysql_conn)
