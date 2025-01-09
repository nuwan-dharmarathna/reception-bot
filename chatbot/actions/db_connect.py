import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Connection string details
connection_string = os.getenv("DB_CONNECTION_STRING")

def db_connection():
    try:
        # Establishing the connection
        conn = psycopg2.connect(connection_string)
        
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        
        # Print PostgreSQL server information
        print("Connected to the database successfully!")
        
        # Return the connection and cursor objects
        return conn, cursor

    except Exception as e:
        print("Error while connecting to the database:", e)
        return None, None


def insert_data():
    
    
    try:
        # Establish the database connection
        conn, cursor = db_connection()
        
        if conn and cursor:
            # Create a table named 'menu'
            create_table_query = """
            CREATE TABLE IF NOT EXISTS menu (
                item_id SERIAL PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                description TEXT,
                price NUMERIC(10, 2) NOT NULL,
                availability BOOLEAN DEFAULT TRUE
            );
            """
            cursor.execute(create_table_query)
            conn.commit()
            print("Table 'menu' created successfully!")

            # Insert some data into the 'menu' table
            insert_data_query = """
            INSERT INTO menu (item_name, description, price, availability)
            VALUES 
                ('Margherita Pizza', 'Classic cheese pizza with fresh tomato sauce', 8.99, TRUE),
                ('Pepperoni Pizza', 'Pizza topped with spicy pepperoni slices', 10.99, TRUE),
                ('Vegetarian Pizza', 'Pizza loaded with fresh vegetables', 9.49, TRUE),
                ('Chicken Burger', 'Grilled chicken burger with lettuce and mayo', 7.99, TRUE),
                ('Choco Donut', 'Freshly baked assorted donuts', 1.99, TRUE),
                ('French Fries', 'Crispy fried potato fries', 2.49, TRUE),
                ('Chocolate Cake', 'Rich chocolate dessert', 4.99, TRUE);
            """
            cursor.execute(insert_data_query)
            conn.commit()
            print("Data inserted successfully into 'menu' table!")

        else:
            print("Unable to connect to the database.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Database connection closed.")

# if __name__ == "__main__":
#     insert_data()
