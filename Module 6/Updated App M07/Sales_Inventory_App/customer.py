import sqlite3
import os

class Customer:
    def __init__(self):
        self.db_path = 'inventory.db'
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_customer(self, customer_name, customer_address, customer_status=1, customer_notes=""):
        """Create a new customer record in the customers table."""
        self.connect()
        try:
            self.cursor.execute(
                '''INSERT INTO customers (customer_name, customer_address, customer_status, customer_notes) VALUES (?, ?, ?, ?)''',
                (customer_name, customer_address, customer_status, customer_notes)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating customer: {e}")
        finally:
            self.disconnect()

    def get_customer(self, customer_id=None):
        """Fetch customer data, optionally filtered by customer ID."""
        self.connect()
        try:
            if customer_id:
                self.cursor.execute('SELECT * FROM customers WHERE customer_ID = ?', (customer_id,))
                return self.cursor.fetchone()
            else:
                self.cursor.execute('SELECT * FROM customers')
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching customers: {e}")
            return []
        finally:
            self.disconnect()

    def update_customer(self, customer_id, customer_name, customer_address, customer_status, customer_notes):
        """Update an existing customer record."""
        self.connect()
        try:
            self.cursor.execute(
                '''UPDATE customers SET customer_name = ?, customer_address = ?, customer_status = ?, customer_notes = ? WHERE customer_ID = ?''',
                (customer_name, customer_address, customer_status, customer_notes, customer_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating customer ID {customer_id}: {e}")
        finally:
            self.disconnect()

    def delete_customer(self, customer_id):
        """Delete a customer from the customers table."""
        self.connect()
        try:
            self.cursor.execute('DELETE FROM customers WHERE customer_ID = ?', (customer_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting customer ID {customer_id}: {e}")
        finally:
            self.disconnect()


import sqlite3
import os

class CustomerHandler:
    def __init__(self):
        self.db_path = 'inventory.db'
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_customer(self, customer_name, customer_address, customer_status=1, customer_notes=""):
        """Create a new customer record in the customers table."""
        self.connect()
        try:
            self.cursor.execute(
                '''INSERT INTO customers (customer_name, customer_address, customer_status, customer_notes) VALUES (?, ?, ?, ?)''',
                (customer_name, customer_address, customer_status, customer_notes)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating customer: {e}")
        finally:
            self.disconnect()

    def get_customer(self, customer_id=None):
        """Fetch customer data, optionally filtered by customer ID."""
        self.connect()
        try:
            if customer_id:
                self.cursor.execute('SELECT * FROM customers WHERE customer_ID = ?', (customer_id,))
                return self.cursor.fetchone()
            else:
                self.cursor.execute('SELECT * FROM customers')
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching customers: {e}")
            return []
        finally:
            self.disconnect()

    def update_customer(self, customer_id, customer_name, customer_address, customer_status, customer_notes):
        """Update an existing customer record."""
        self.connect()
        try:
            self.cursor.execute(
                '''UPDATE customers SET customer_name = ?, customer_address = ?, customer_status = ?, customer_notes = ? WHERE customer_ID = ?''',
                (customer_name, customer_address, customer_status, customer_notes, customer_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating customer ID {customer_id}: {e}")
        finally:
            self.disconnect()

    def delete_customer(self, customer_id):
        """Delete a customer from the customers table."""
        self.connect()
        try:
            self.cursor.execute('DELETE FROM customers WHERE customer_ID = ?', (customer_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting customer ID {customer_id}: {e}")
        finally:
            self.disconnect()
