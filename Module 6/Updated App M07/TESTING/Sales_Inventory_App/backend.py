import sqlite3
import os

class Backend:
    def __init__(self):
        self.db_path = 'inventory.db'
        self.conn = None
        self.cursor = None

    def create_database(self):
        """Creates the necessary tables if they do not exist."""
        if not os.path.exists(self.db_path):
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self._create_users_table()
            self._create_inventory_table()
            self._create_customers_table()
            self._create_sales_table()
            self._create_sales_items_table()
            self.conn.commit()
            self.conn.close()

    def _create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                date_created DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    def _create_inventory_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                size TEXT NOT NULL,
                quantity INTEGER,
                price DECIMAL(10, 2) NOT NULL,
                date_added DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    def _create_customers_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_address TEXT NOT NULL,
                customer_status INTEGER,
                customer_notes TEXT,
                date_order DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    def _create_sales_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                user_ID INTEGER NOT NULL,
                customer_ID INTEGER NOT NULL,
                grand_total DECIMAL(10, 2),
                date_sale DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_ID) REFERENCES users(user_ID),
                FOREIGN KEY (customer_ID) REFERENCES customers(customer_ID)
            )
        ''')

    def _create_sales_items_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales_items (
                sale_item_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_ID INTEGER NOT NULL,
                item_ID INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (sale_ID) REFERENCES sales(sale_ID),
                FOREIGN KEY (item_ID) REFERENCES items(item_ID)
            )
        ''')

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def get_all_users(self):
        """Fetch all users from the users table."""
        self.connect()
        try:
            self.cursor.execute('SELECT username FROM users')
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error fetching users: {e}")
            return []
        finally:
            self.disconnect()

    def delete_user(self, username):
        """Delete a user from the users table."""
        self.connect()
        try:
            self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting user '{username}': {e}")
        finally:
            self.disconnect()
