from db_handle import connection
from mysql.connector import Error

def execute_query(query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('✅ Query executed successfully')
    except Error as e:
        print('❌ Query failed', e)
    finally:
        cursor.close()

# SQL query to create tables

customers_table = """
    CREATE TABLE customer(
        cus_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(30) NOT NULL,
        last_name VARCHAR(30) NOT NULL,
        phone_number VARCHAR(255) NOT NULL UNIQUE
    )
"""

menu_table = """
    CREATE TABLE menu(
        id INT AUTO_INCREMENT PRIMARY KEY,
        menu_name VARCHAR(30) NOT NULL UNIQUE,
        description TEXT
    )
"""

menu_items_table = """
    CREATE TABLE menu_item(
        item_id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(30) NOT NULL UNIQUE,
        price DECIMAL(10, 2) NOT NULL,
        description TEXT,
        status ENUM('available', 'unavailable') NOT NULL DEFAULT 'available',
        menu_id INT NOT NULL,
        FOREIGN KEY (menu_id) REFERENCES menu(id)
    )
"""

orders_table = """
    CREATE TABLE orders(
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        cus_id INT NOT NULL,
        total DECIMAL(10, 2) NOT NULL,
        order_date DATE NOT NULL,
        order_type ENUM('dine-in', 'take-out') NOT NULL DEFAULT 'take-out',
        FOREIGN KEY (cus_id) REFERENCES customer(cus_id)
    )
"""

order_items_table = """
    CREATE TABLE order_item(
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        item_id INT NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (item_id) REFERENCES menu_item(item_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
"""

reservation_table = """
    CREATE TABLE reservation(
        reservation_id INT AUTO_INCREMENT PRIMARY KEY,
        cus_id INT NOT NULL,
        reservation_date DATE NOT NULL,
        reservation_time TIME NOT NULL,
        guests INT NOT NULL,
        FOREIGN KEY (cus_id) REFERENCES customer(cus_id)
    )
"""

table_table = """
    CREATE TABLE restaurant_table(
        id INT AUTO_INCREMENT PRIMARY KEY,
        table_number INT NOT NULL UNIQUE,
        capacity INT NOT NULL,
        status ENUM('occupied', 'available') NOT NULL DEFAULT 'available'
    )
"""

payment_table = """
    CREATE TABLE payment(
        payment_id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        payment_date DATE NOT NULL,
        payment_time TIME NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        payment_method ENUM('cash', 'card') NOT NULL DEFAULT 'cash',
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
"""


# Execute the queries
execute_query(customers_table)
execute_query(menu_table)
execute_query(menu_items_table)
execute_query(orders_table)
execute_query(order_items_table)
execute_query(reservation_table)
execute_query(table_table)
execute_query(payment_table)

# Close the connection
connection.close()
