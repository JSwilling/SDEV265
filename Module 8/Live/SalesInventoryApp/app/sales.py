import sqlite3
import os

class Sales:
    def __init__(self):
        self.db_path = 'db/Sales_Inventory.db'
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_sales(self, user_id, customer_id, items):
        """Create a new sale in the sales table and corresponding items in sales_items."""
        self.connect()
        try:
            # Insert new sale record
            self.cursor.execute(
                '''INSERT INTO sales (user_ID, customer_ID, grand_total) VALUES (?, ?, ?)''',
                (user_id, customer_id, sum(item['price'] * item['quantity'] for item in items))
            )
            sale_id = self.cursor.lastrowid

            # Insert each item into sales_items table
            for item in items:
                self.cursor.execute(
                    '''INSERT INTO sales_items (sale_ID, item_ID, quantity, price) VALUES (?, ?, ?, ?)''',
                    (sale_id, item['item_id'], item['quantity'], item['price'])
                )

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating sale: {e}")
        finally:
            self.disconnect()

    def get_sales(self, sale_id=None):
        """Fetch sales data, optionally filtered by sale ID."""
        self.connect()
        try:
            if sale_id:
                self.cursor.execute('SELECT * FROM sales WHERE sale_ID = ?', (sale_id,))
                return self.cursor.fetchone()
            else:
                self.cursor.execute('SELECT * FROM sales')
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching sales: {e}")
            return []
        finally:
            self.disconnect()

    def get_sales_items(self, sale_id):
        """Fetch all items related to a specific sale."""
        self.connect()
        try:
            self.cursor.execute('SELECT * FROM sales_items WHERE sale_ID = ?', (sale_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching sales items for sale ID {sale_id}: {e}")
            return []
        finally:
            self.disconnect()

    def delete_sale(self, sale_id):
        """Delete a sale and corresponding items from the database."""
        self.connect()
        try:
            # Delete items related to the sale
            self.cursor.execute('DELETE FROM sales_items WHERE sale_ID = ?', (sale_id,))
            # Delete the sale
            self.cursor.execute('DELETE FROM sales WHERE sale_ID = ?', (sale_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting sale ID {sale_id}: {e}")
        finally:
            self.disconnect()


import sqlite3
import os

class SalesHandler:
    def __init__(self):
        self.db_path = 'db/Sales_Inventory.db'
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_sale(self, user_id, customer_id, items):
        """Create a new sale in the sales table and corresponding items in sales_items."""
        self.connect()
        try:
            # Insert new sale record
            self.cursor.execute(
                '''INSERT INTO sales (user_ID, customer_ID, grand_total) VALUES (?, ?, ?)''',
                (user_id, customer_id, sum(item['price'] * item['quantity'] for item in items))
            )
            sale_id = self.cursor.lastrowid

            # Insert each item into sales_items table
            for item in items:
                self.cursor.execute(
                    '''INSERT INTO sales_items (sale_ID, item_ID, quantity, price) VALUES (?, ?, ?, ?)''',
                    (sale_id, item['item_id'], item['quantity'], item['price'])
                )

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating sale: {e}")
        finally:
            self.disconnect()

    def get_sales(self, sale_id=None):
        """Fetch sales data, optionally filtered by sale ID."""
        self.connect()
        try:
            if sale_id:
                self.cursor.execute('SELECT * FROM sales WHERE sale_ID = ?', (sale_id,))
                return self.cursor.fetchone()
            else:
                self.cursor.execute('SELECT * FROM sales')
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching sales: {e}")
            return []
        finally:
            self.disconnect()

    def get_sales_items(self, sale_id):
        """Fetch all items related to a specific sale."""
        self.connect()
        try:
            self.cursor.execute('SELECT * FROM sales_items WHERE sale_ID = ?', (sale_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching sales items for sale ID {sale_id}: {e}")
            return []
        finally:
            self.disconnect()

    def delete_sale(self, sale_id):
        """Delete a sale and corresponding items from the database."""
        self.connect()
        try:
            # Delete items related to the sale
            self.cursor.execute('DELETE FROM sales_items WHERE sale_ID = ?', (sale_id,))
            # Delete the sale
            self.cursor.execute('DELETE FROM sales WHERE sale_ID = ?', (sale_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting sale ID {sale_id}: {e}")
        finally:
            self.disconnect()
