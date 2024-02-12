CREATE TABLE category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE product_unit (
    unit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20) NOT NULL
);

CREATE TABLE product (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category_id INT,
    unit_id INTEGER,
    product_image VARCHAR(255),
    FOREIGN KEY (category_id) REFERENCES category(category_id),
    FOREIGN KEY (unit_id) REFERENCES product_unit(unit_id)
);

CREATE TABLE shop_list (
    shop_list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE shop_list_product (
    shop_list_id INTEGER,
    product_id INTEGER,
    quantity INTEGER NOT NULL,
    category_id INTEGER,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (shop_list_id, product_id),
    FOREIGN KEY (shop_list_id) REFERENCES shop_list(shop_list_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    FOREIGN KEY (category_id) REFERENCES category(category_id)
);
