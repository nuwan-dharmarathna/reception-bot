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
