from mysql.connector import Error
import mysql.connector

import os 
from dotenv import load_dotenv

from datetime import datetime

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
            WHERE m.menu_name IN (%s, 'bakery items', 'juices')
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
    
    