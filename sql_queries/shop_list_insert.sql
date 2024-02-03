-- Insert categories
INSERT INTO category (name)
VALUES
    ('Electronics'),
    ('Clothing'),
    ('Groceries'),
    ('Furniture'),
    ('Beauty and Personal Care');
    
    
-- Insert products with corresponding categories
INSERT INTO product (name, price, category_id, product_image)
VALUES
    ('Smartphone', 599.99, 1),
    ('Laptop', 899.99, 1),
    ('T-shirt', 19.99, 2),
    ('Jeans', 39.99, 2),
    ('Milk', 2.99, 3),
    ('Sofa', 499.99, 4),
    ('Shampoo', 8.99, 5),
    ('Toothpaste', 3.49, 5);
    
-- Insert shop lists
INSERT INTO shop_list (name)
VALUES
    ('Grocery List'),
    ('Tech Shopping'),
    ('Clothing Shopping');
    
    
-- Insert products into shop lists with quantities and categories
INSERT INTO shop_list_product (shop_list_id, product_id, quantity, category_id)
VALUES
    (1, 5, 3, 3),    -- Milk
    (1, 6, 2, 4),    -- Sofa
    (2, 1, 1, 1),    -- Smartphone
    (2, 2, 2, 1),    -- Laptop
    (3, 3, 5, 2),    -- T-shirt
    (3, 4, 4, 2);    -- Jeans