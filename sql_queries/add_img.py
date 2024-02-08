import os
import mysql.connector
from decouple import config

conn = mysql.connector.connect(
    host=config('DB_HOST'),
    user=config('DB_USER'),
    password=config('DB_PASSWORD'),
    database='shopping_list_db'
)

path = os.path.join(os.getcwd(), '..', 'png')

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
    img_path = os.path.join(os.getcwd(), '..', 'png', image_filename)
    cursor.execute("SELECT product_image FROM product WHERE name = %s", (product_name,))
    curr_val = cursor.fetchone()[0]

    if curr_val is None:
        update_query = "UPDATE product SET product_image = %s WHERE name = %s"
        cursor.execute(update_query, (img_path, product_name))
        print(f'UPDATED - Product {product_name} contains {img_path}')
    else:
        print(f'SKIPPED - Product {product_name} already contains {curr_val}')

conn.commit()
cursor.close()
conn.close()
