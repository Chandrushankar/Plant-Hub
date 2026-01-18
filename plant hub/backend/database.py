import mysql.connector
from mysql.connector import Error
import os

# Database Configuration (Ideally from env vars)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password', # User must replace this
    'database': 'plant_hub'
}

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None
