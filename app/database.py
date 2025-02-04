import sqlite3
import threading

class Database:

    DB_NAME = "data/database.db"
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):   
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        with self._lock:
            if not self._initialized:
                try:
                    self.connection = sqlite3.connect(self.DB_NAME, check_same_thread=False)
                    self.cursor = self.connection.cursor()
                    self._initialized = True
                except sqlite3.Error as e:
                    print(f"Database connection error: {e}")

    def create_table(self, table_name, columns, constraint=""):
        """
        Create a table if it doesn't exist.
        :param table_name: Name of the table.
        :param columns: Dictionary of column names and their data types.
        """
        columns_with_types = ', '.join([f'{col} {dtype}' for col, dtype in columns.items()])
        if constraint:
            constraint = f", {constraint}"
        self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {columns_with_types} {constraint})')
        self.connection.commit()
    
    def execute_query(self, query, params=()):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            self.connection.rollback()

    def fetch_all(self, table_name, condition=None, params=()):
        """
        Fetch all records from the table.
        :param table_name: Name of the table.
        :param condition: Optional condition for filtering (e.g., "column = ?").
        :param params: Parameters for the condition.
        :return: List of records.
        """
        query = f'SELECT * FROM {table_name}'
        if condition:
            query += f' WHERE {condition}'
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, table_name, condition, params=()):
        """
        Fetch a single record from the table.
        :param table_name: Name of the table.
        :param condition: Condition for filtering (e.g., "column = ?").
        :param params: Parameters for the condition.
        :return: A single record or None if not found.
        """
        query = f'SELECT * FROM {table_name} WHERE {condition}'
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def search(self, table_name, fields={},):
        """
        Search DB for matching records
        :param table_name: Name of the table.
        :param fields: Dictionnary of filds name as keys and value to match with 
        """
        if not fields:
            return self.fetch_all(table_name)

        vals = []
        conditions = []
        for key, value in fields.items():
            conditions.append(f"{key} LIKE ?")
            vals.append(f"%{value}%")

        conditions_str = ' OR '.join(conditions)
        query = f'SELECT * FROM {table_name} WHERE {conditions_str}'
        self.cursor.execute(query, tuple(vals))
        return self.cursor.fetchall()

    def record_exists(self, table_name, column, value):
        """
        Check if a record exists in the table based on a column and value.
        :param table_name: Name of the table.
        :param column: Column to check.
        :param value: Value to check in the column.
        :return: True if the record exists, False otherwise.
        """
        query = f'SELECT COUNT(*) FROM {table_name} WHERE {column} = ?'
        self.cursor.execute(query, (value,))
        result = self.cursor.fetchone()
        return result[0] > 0
    
    def insert(self, table_name, data):
        """
        Insert a record into the table.
        :param table_name: Name of the table.
        :param data: Dictionary of column names and their values.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        self.cursor.execute(query, tuple(data.values()))
        self.connection.commit()

    def update(self, table_name, data, condition, params=()):
        """
        Update records in the table.
        :param table_name: Name of the table.
        :param data: Dictionary of column names and their new values.
        :param condition: Condition for updating (e.g., "id = ?").
        :param params: Parameters for the condition.
        """
        updates = ', '.join([f'{col} = ?' for col in data.keys()])
        query = f'UPDATE {table_name} SET {updates} WHERE {condition}'
        self.cursor.execute(query, tuple(data.values()) + tuple(params))
        self.connection.commit()

    def delete(self, table_name, condition, params=()):
        """
        Delete records from the table.
        :param table_name: Name of the table.
        :param condition: Condition for deletion (e.g., "id = ?").
        :param params: Parameters for the condition.
        """
        query = f'DELETE FROM {table_name} WHERE {condition}'
        self.cursor.execute(query, params)
        self.connection.commit()

    def close(self):
        self.connection.close()

    def __del__(self):
        self.close()

if __name__ == "__main__":
    Database().s