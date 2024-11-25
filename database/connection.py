import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    def __init__(self):
        self.connection = None
        
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',  # Replace with your MySQL username
                password='',  # Replace with your MySQL password
                database='library_db'
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to MySQL Database: {e}")
            return False
            
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            
    def get_connection(self):
        """Get the database connection object"""
        return self.connection

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.connection.commit()
                return cursor.lastrowid
            else:
                return cursor.fetchall()
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
