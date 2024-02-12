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

INSERT INTO shop_list (name)
VALUES ('Grocery List'),
       ('Tech Shopping'),
       ('Clothing Shopping');


INSERT INTO shop_list_product (shop_list_id, product_id, quantity, category_id)
VALUES (1, 5, 3, 3),
       (1, 6, 2, 4),
       (1, 7, 2, 5),
       (1, 8, 3, 5),
       (1, 9, 2, 1),
       (1, 10, 1, 2),
       (2, 1, 1, 1),
       (2, 2, 2, 1),
       (2, 3, 2, 2),
       (2, 5, 1, 3),
       (2, 7, 1, 5),
       (2, 8, 2, 5),
       (3, 3, 5, 2),
       (3, 4, 4, 2),
       (3, 1, 1, 1),
       (3, 6, 1, 4),
       (3, 7, 1, 5),
       (3, 10, 1, 2);
