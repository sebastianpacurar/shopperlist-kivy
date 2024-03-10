INSERT INTO user (name, email, password, online_status)
VALUES ('user', 'user@example.com', '1234', 0),
       ('user2', 'user2@example.com', '1234', 0);


INSERT INTO category (name)
VALUES ('Electronics'),
       ('Clothing'),
       ('Groceries'),
       ('Furniture'),
       ('Beauty and Personal Care');


INSERT INTO product_unit (name)
VALUES ('L'),
       ('Kg'),
       ('Piece'),
       ('Pair'),
       ('Gr');


INSERT INTO product (name, price, unit_id, category_id)
VALUES ('Smartphone', 599.99, 3, 1),
       ('Laptop', 899.99, 3, 1),
       ('T-shirt', 19.99, 3, 2),
       ('Jeans', 39.99, 3, 2),
       ('Milk', 2.99, 1, 3),
       ('Sofa', 499.99, 3, 4),
       ('Shampoo', 8.99, 3, 5),
       ('Toothpaste', 3.49, 5, 5),
       ('Headphones', 59.99, 3, 1),
       ('Running Shoes', 69.99, 3, 2),
       ('Coffee', 4.99, 3, 3),
       ('Chocolate', 3.99, 5, 3);

INSERT INTO shop_list (user_id, name)
VALUES (1, 'Grocery List'),
       (1, 'Tech Shopping'),
       (1, 'Clothing Shopping');


INSERT INTO shop_list_product (shop_list_id, product_id, quantity, unit_id, category_id, active)
VALUES
-- Grocery List
(1, 1, 1, 3, 1, 0),
(1, 2, 1, 3, 1, 0),
(1, 3, 1, 3, 2, 0),
(1, 4, 1, 3, 2, 0),
(1, 5, 1, 1, 3, 0),
(1, 6, 1, 3, 4, 0),

-- Tech Shopping
(2, 7, 1, 3, 5, 0),
(2, 8, 1, 5, 5, 0),
(2, 9, 1, 3, 1, 0),
(2, 10, 1, 3, 2, 0),
(2, 11, 1, 3, 3, 0),
(2, 12, 1, 5, 3, 0),
-- Clothing Shopping
(3, 1, 1, 3, 1, 0),
(3, 2, 1, 3, 1, 0),
(3, 3, 1, 3, 2, 0),
(3, 4, 1, 3, 2, 0),
(3, 5, 1, 1, 3, 0),
(3, 6, 1, 3, 4, 0),
(3, 7, 1, 3, 5, 0),
(3, 8, 1, 5, 5, 0),
(3, 9, 1, 3, 1, 0),
(3, 10, 1, 3, 2, 0),
(3, 11, 1, 3, 3, 0),
(3, 12, 1, 5, 3, 0);

