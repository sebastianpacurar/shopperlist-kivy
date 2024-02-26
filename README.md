# Shopper List Kivy Showcase

- A project made with Kivy and SQL, using the KivyMD material design extension
- Simulates a shopping list, allowing users to create/filter products, create lists, login/register

## Table of Contents

- [Setup](#Setup)
- [DB Setup](#DB-Setup)
- [Run](#Run)
- [Additional Info](#Additional-Info)


### Setup

To get started with this project, follow these steps:

1. Clone or download and change directory to app's location, sing a terminal/shell.
2. Create a virtual environment:
    ```
    python3 -m venv my_venv
    ```
   
3. Activate the virtual environment by executing the following command:
   - Windows users: `my_venv\Scripts\activate`
   - Linux/Mac users: `source my_venv/bin/activate`
   
4. Install dependencies using pip from active venv:
    ```
    pip install -r requirements.txt
    ```

### DB Setup
- The app supports both **Sqlite3** and **MySql**.
- **Sqlite3** is enabled by default.

1. Sqlite3 setup:
   - To recreate the Sqlite3 db go to `setup/` folder and run `setup_sqlite.py`.

2. MySql setup:
   1. Create a db named `shopping_list_db` on your MySql server.
   2. Create the tables using `mysql_tables.sql` query file from `setup/sql/` folder.
   3. Insert data into the tables using `insert_data.sql` query file from `setup/sql/` folder.
   4. Create a `.env` file in the root folder with the following contents:
      ```
      DB_HOST=<host>
      DB_USER=<user>
      DB_PASSWORD=<pass>
      ```
      - Replace **host** with your host (eg: localhost).
      - Replace **user** and **pass** with the creds used to create the db at step 1.
   5. Run the `add_img.py` script from `setup/` folder (this populates the product img_path column)
   6. Change line 19 of `components.py` script from `app/components/` with the following:
      ```
      db = Database(MYSQL)
      ```

### Run
1. From root folder change directory to `app/` and run `main.py`:
    ```
    cd app
    python main.py
    ```
   
2. Log in using the following users:
   <br>`user1` with password: `1234`<br>
   `user2` with password: `1234`
3. Alternatively, users can be created using fake emails, from the Register Screen

### Additional Info
- Login with Google does not work
- Currently, the **main branch** runs under **kivymd 1.2.0** which is pretty deprecated.
- Migration to **kivymd 2.0.1dev0** is in progress


