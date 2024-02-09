-- Insert categories
INSERT INTO category (name)
VALUES ('Electronics'),
       ('Clothing'),
       ('Groceries'),
       ('Furniture'),
       ('Beauty and Personal Care');


-- Insert products with corresponding categories
INSERT INTO product (name, price, unit, category_id)
VALUES ('Smartphone', 599.99, 'piece', 1),
       ('Laptop', 899.99, 'piece', 1),
       ('T-shirt', 19.99, 'piece', 2),
       ('Jeans', 39.99, 'piece', 2),
       ('Milk', 2.99, 'L', 3),
       ('Sofa', 499.99, 'piece', 4),
       ('Shampoo', 8.99, 'piece', 5),
       ('Toothpaste', 3.49, 'piece', 5),
       ('Headphones', 59.99, 'piece', 1),
       ('Running Shoes', 69.99, 'pair', 2),
       ('Coffee', 4.99, 'piece', 3),
       ('Chocolate', 3.99, 'piece', 3);

-- Insert shop lists
INSERT INTO shop_list (name)
VALUES ('Grocery List'),
       ('Tech Shopping'),
       ('Clothing Shopping');


-- Insert products into shop lists with quantities and categories
INSERT INTO shop_list_product (shop_list_id, product_id, quantity, category_id)
VALUES (1, 5, 3, 3),  -- Milk
       (1, 6, 2, 4),  -- Sofa
       (1, 7, 2, 5),  -- Shampoo
       (1, 8, 3, 5),  -- Toothpaste
       (1, 9, 2, 1),  -- Headphones
       (1, 10, 1, 2), -- Running Shoes
       (2, 1, 1, 1),  -- Smartphone
       (2, 2, 2, 1),  -- Laptop
       (2, 3, 2, 2),  -- T-shirt
       (2, 5, 1, 3),  -- Milk
       (2, 7, 1, 5),  -- Shampoo
       (2, 8, 2, 5),  -- Toothpaste
       (3, 3, 5, 2),  -- T-shirt
       (3, 4, 4, 2),  -- Jeans
       (3, 1, 1, 1),  -- Smartphone
       (3, 6, 1, 4),  -- Sofa
       (3, 7, 1, 5),  -- Shampoo
       (3, 10, 1, 2); -- Running Shoes