import mysql.connector
from mysql.connector import Error
from utils.config_reader import ConfigReader

class DatabaseConnection:
    def __init__(self):
        self.config = ConfigReader.get_db_config()
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                port=self.config['port'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            raise Exception(f"Database connection error: {str(e)}")
        return None

    def execute_query(self, query, params=None):
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            raise Exception(f"Query execution error: {str(e)}")
        finally:
            cursor.close()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
