import mysql.connector
from mysql.connector import Error

def save_to_db(S, K, T, r, sigma, option_type, price):
    try:
        # Establish the connection to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",        # Use "localhost" if your MySQL is running locally
            user="root",             # Replace with your MySQL username
            password="Aldarita0", # Replace with your MySQL password
            database="options_pricing_db"  # Replace with your database name
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            # SQL query to insert the data into the table
            insert_query = """
                INSERT INTO options_pricing (stock_price, strike_price, time_to_expiry, interest_rate, volatility, option_type, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Data to insert
            data = (S, K, T, r, sigma, option_type, price)
            
            # Execute the query
            cursor.execute(insert_query, data)
            
            # Commit the transaction
            conn.commit()
            print("Data saved successfully.")
    
    except Error as e:
        # Print any error that occurs during the connection or execution
        print(f"Error: {e}")
    
    finally:
        # Ensure that the cursor and connection are properly closed
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection closed.")