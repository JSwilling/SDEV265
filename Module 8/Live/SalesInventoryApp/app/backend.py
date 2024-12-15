import sqlite3
import os

class Backend:
    def __init__(self):
        self.db_path = r'db/Sales_Inventory.db'
        self.conn = None
        self.cursor = None

    def create_database(self):
        """Creates or recreates the necessary tables."""
        self.connect()  # Ensure the connection is open
        try:
            # Create the tables
            self._create_users_table()
            self._create_customers_table()
            self._create_inventory_items_table()
            self._create_orders_table()
            self._create_clock_times_table()
            self._create_user_activity_table()
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating database schema: {e}")
            raise  # Re-raise the exception for the calling method to handle

    def _create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

    def _create_customers_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customer (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        ''')

    def _create_inventory_items_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS InventoryItem (
                item_id INTEGER PRIMARY KEY,
                Name TEXT NOT NULL,
                SKU TEXT NOT NULL,
                price REAL NOT NULL,
                stockLevel INTEGER NOT NULL
            )
        ''')

    def _create_orders_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY,
                order_date TEXT NOT NULL,
                customer TEXT NOT NULL,
                item_id TEXT NOT NULL,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                delivery_address TEXT NOT NULL,
                contact TEXT NOT NULL,
                notes TEXT,
                agent_id TEXT NOT NULL
            )
        ''')

    def _create_transactions_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transaction (
                transaction_id TEXT PRIMARY KEY,
                item_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (item_id) REFERENCES InventoryItem(item_id),
                FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
            )
        ''')

    def _create_clock_times_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clock_times (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                clock_in DATETIME NOT NULL,
                clock_out DATETIME
            )
        ''')

    def _create_user_activity_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                timestamp DATETIME NOT NULL
            )
        ''')

    def get_highest_priced_orders(self):
        """Fetch highest-priced orders and their stock levels."""
        self.connect()
        try:
            query = '''
            SELECT 
                i.item_id, 
                i.Name AS product, 
                SUM(o.quantity) AS quantity_ordered, 
                i.stockLevel AS stock_level, 
                i.price
            FROM InventoryItem i
            LEFT JOIN Orders o ON i.item_id = o.item_id
            GROUP BY i.item_id
            ORDER BY i.price DESC
            LIMIT 10;
            '''
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching highest-priced orders: {e}")
            return []
        finally:
            self.disconnect()

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


    def connect(self):
        """Creates a connection to the SQLite database."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Closes the connection to the SQLite database."""
        if self.conn:
            self.conn.close()
