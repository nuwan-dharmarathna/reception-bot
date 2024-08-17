from mysql.connector import Error
import mysql.connector

import os 
from dotenv import load_dotenv


load_dotenv()

DATABASE_NAME = 'restaurant_db'

try:
    connection = mysql.connector.connect(
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        host = os.getenv('DB_HOST'),
        database = DATABASE_NAME
    )
    
    if connection.is_connected():
        print(f'✅ Connected to {DATABASE_NAME} database')
except Error as e:
    print('❌ Connection failed', e)


def show_menu(meal_time:str):
    try:
        # create a cursor object
        cursor = connection.cursor()
            
        # Query the database for the menu
        query = """
            SELECT m.menu_name, mi.item_name, mi.price, mi.status
            FROM menu_item mi
            INNER JOIN menu m ON mi.menu_id = m.id
            WHERE m.menu_name IN (%s, 'bakery items', 'juices') AND mi.status = 'available'
            GROUP BY mi.item_name, mi.price, mi.status
        """
        
        cursor.execute(query, (meal_time,))
        
        result = cursor.fetchall()
        
        cursor.close()
        
        if not result:
            return "No items available at the moment"
        else:
            return result
    except Error as e:
        print('❌ Error occured', e)
        return "❌ An error occured while fetching the menu"

def calc_tot_price():
    pass    

def check_order_item(food_items:list, quantity:list, meal_time:str):
    try:
        # create cursor object
        cursor = connection.cursor()
        
        # Initialize result list
        keys_to_delete = []
        
        # Query the database for the menu
        query = """
            SELECT mi.item_name, mi.price
            FROM menu_item mi
            INNER JOIN menu m ON mi.menu_id = m.id
            WHERE m.menu_name IN (%s, 'bakery items', 'juices') AND mi.item_name IN (%s)
        """
        
        #create an order dict
        order_dict = dict(zip(food_items, quantity))
        
        order_dict_with_price = {}
        
        for key in order_dict.keys():
            cursor.execute(query, (meal_time, key))
            
            result = cursor.fetchall()
            
            if not result:
                print(f"{key} is not available at the menu")
                keys_to_delete.append(key)
            else:
                # print(f"{key}:{result[0][1]}, {result}")
                # print(f"qty: {order_dict[key]}")
                
                # calculate sub tot
                sub_tot = float(result[0][1]) * order_dict[key]
                
                order_dict_with_price[key] = {
                    'quantity': order_dict[key],
                    'item_price': float(result[0][1]),
                    'sub_tot': sub_tot
                }
                
        
        # remove items not in menu
        if len(keys_to_delete) > 0:
            for key in keys_to_delete:
                del order_dict[key]

        return order_dict_with_price
            
    except Error as e:
        print('❌ Error occured', e)
        return "❌ An error occured while fetching the menu"
    
    finally:
        cursor.close()

def get_next_order_id():
    try:
        # create cursor object
        cursor = connection.cursor()
        
        # Query the database for the next order id
        query = """
            SELECT MAX(order_id) FROM orders
        """
        
        cursor.execute(query)
        
        result = cursor.fetchone()
        
        cursor.close()
        
        if not result:
            return -1
        else:
            return result[0] + 1
        
    except Error as e:
        print('❌ Error occured', e)
        return "❌ An error occured while fetching the menu"

def complete_order(order: dict):
    # Get the next order id
    order_id = get_next_order_id()
    
    