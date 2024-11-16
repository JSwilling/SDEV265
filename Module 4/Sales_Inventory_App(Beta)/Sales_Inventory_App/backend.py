import sqlite3

class Backend:
    def __init__(self):
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        self.create_inventory_table()
        self.create_users_table()  # Create users table for termination functionality
        self.inventory_data = [
            {"name": "Laptop", "quantity": 120},
            {"name": "Smartphone", "quantity": 250},
            {"name": "Tablet", "quantity": 80},
            {"name": "Monitor", "quantity": 150},
            {"name": "Keyboard", "quantity": 300},
            {"name": "Mouse", "quantity": 275},
            {"name": "Headphones", "quantity": 180},
            {"name": "External HDD", "quantity": 90},
            {"name": "Router", "quantity": 60},
            {"name": "Printer", "quantity": 40},
        ]

    def create_inventory_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                item_id TEXT PRIMARY KEY,
                order_id TEXT,
                customer_name TEXT,
                address TEXT,
                status TEXT,
                quantity INTEGER,
                notes TEXT
            )
        ''')
        self.conn.commit()

    def create_users_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password BLOB NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def save_inventory(self, data):
        self.cursor.execute('''
            INSERT OR REPLACE INTO inventory (item_id, order_id, customer_name, address, status, quantity, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['item_id'], data['order_id'], data['customer_name'], data['address'], data['status'], data['quantity'], data['notes']))
        self.conn.commit()

    def query_inventory(self, item_id):
        self.cursor.execute('SELECT * FROM inventory WHERE item_id = ?', (item_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                "item_id": row[0],
                "order_id": row[1],
                "customer_name": row[2],
                "address": row[3],
                "status": row[4],
                "quantity": row[5],
                "notes": row[6]
            }
        return None

    def get_inventory_data(self):
        """Returns the inventory data."""
        return self.inventory_data

    def update_inventory(self, item_name, quantity):
        """Updates the inventory quantity for a given item name."""
        for item in self.inventory_data:
            if item["name"] == item_name:
                item["quantity"] = quantity
                return True
        return False

    def add_inventory_item(self, item_name, quantity):
        """Adds a new inventory item."""
        self.inventory_data.append({"name": item_name, "quantity": quantity})

    def delete_inventory_item(self, item_name):
        """Deletes an inventory item by its name."""
        self.inventory_data = [item for item in self.inventory_data if item["name"] != item_name]

    def get_all_users(self):
        self.cursor.execute('SELECT username FROM users')
        users = [row[0] for row in self.cursor.fetchall()]
        return users

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()