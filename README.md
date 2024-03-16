# Shopper List Kivy Showcase

- A project made with Kivy and SQL, using the KivyMD material design extension
- Simulates a shopping list, allowing users to create/filter products, create lists, login/register

## Table of Contents

- [Setup](#Setup)
- [How To Run](#How-To-Run)
- [DB Setup (optional)](#DB-Setup-optional) 


### Setup

To get started with this project, follow these steps:

1. Install **_Python 3.11_** if required. May not work on earlier versions!
2. Clone or download repo, then change directory to app's location using a terminal/shell.
   - Windows users should use **_cmd_**, instead of **_powershell_** due to ExecutionPolicy restrictions on powershell
3. Create a virtual environment:
    ```
    python3 -m venv my_venv
    ```
   
4. Activate the virtual environment by executing the following command:
   - Windows users: `my_venv\Scripts\activate`
   - Linux/Mac users: `source my_venv/bin/activate`
   
5. Install dependencies using pip from active venv:
    ```
    pip install -r requirements.txt
    ```

6. When done with the app, to deactivate the virtual environment, type `deactivate` in the terminal.


### How To Run
1. From root folder run `main.py` using python command (either **python**, or **python3**, depending on the OS):
   - Linux/Mac users: `python main.py`
   - Windows users: `python3 main.py`
   
2. Log in using the following users:
   <br>`user` with password: `1234`<br>
   `user2` with password: `1234`
3. Alternatively, users can be created using fake emails, from the Register Screen



### DB Setup (optional)
- The app supports both **Sqlite3** and **MySql**.
- **Sqlite3** is enabled by default.

1. Sqlite3 DB Generator:
   - The db gets generated, with default values, when the db file is missing from `db/` folder.
   - To recreate the sqlite3 db, go to `db/` folder and delete `shopping_list_db.db`, then rerun the app.

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
   5. Run the `add_img.py` script from `setup/` folder (this populates the product img_path column).
   6. Change line 19 of `components.py` script from `app/components/` with the following:
      ```
      db = Database(MYSQL)
      ```
