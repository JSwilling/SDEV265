import sqlite3
import os
import csv
from datetime import datetime

class ReportGenerator:
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

    def generate_sales_report(self, start_date=None, end_date=None, output_file='sales_report.csv'):
        """Generate a sales report for a specified date range and save it as a CSV file."""
        self.connect()
        try:
            query = '''
            SELECT sales.sale_id, sales.date, sales.quantity, users.user_id, items.item_name, items.price
            FROM sales
            JOIN users ON sales.user_id = users.user_id
            JOIN items ON sales.item_id = items.item_id
            '''
            params = []
            if start_date and end_date:
                query += ' WHERE date_sale BETWEEN ? AND ?'
                params.extend([start_date, end_date])

            self.cursor.execute(query, params)
            sales_data = self.cursor.fetchall()

            # Write data to CSV
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames = ['Sale ID', 'User', 'Customer', 'Grand Total', 'Date of Sale']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for sale in sales_data:
                    writer.writerow({
                        'Sale ID': sale[0],
                        'User': sale[1],
                        'Customer': sale[2],
                        'Grand Total': sale[3],
                        'Date of Sale': sale[4]
                    })

            print(f"Sales report generated: {output_file}")
        except sqlite3.Error as e:
            print(f"Error generating sales report: {e}")
        finally:
            self.disconnect()

    def generate_inventory_report(self, output_file='inventory_report.csv'):
        """Generate an inventory report and save it as a CSV file."""
        self.connect()
        try:
            self.cursor.execute('SELECT * FROM items')
            items_data = self.cursor.fetchall()

            # Write data to CSV
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames = ['Item ID', 'Product', 'Size', 'Quantity', 'Price', 'Date Added']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for item in items_data:
                    writer.writerow({
                        'Item ID': item[0],
                        'Product': item[1],
                        'Size': item[2],
                        'Quantity': item[3],
                        'Price': item[4],
                        'Date Added': item[5]
                    })

            print(f"Inventory report generated: {output_file}")
        except sqlite3.Error as e:
            print(f"Error generating inventory report: {e}")
        finally:
            self.disconnect()

    def generate_customer_report(self, output_file='customer_report.csv'):
        """Generate a customer report and save it as a CSV file."""
        self.connect()
        try:
            self.cursor.execute('SELECT * FROM customers')
            customers_data = self.cursor.fetchall()

            # Write data to CSV
            with open(output_file, 'w', newline='') as csvfile:
                fieldnames = ['Customer ID', 'Customer Name', 'Address', 'Status', 'Notes', 'Date Order']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for customer in customers_data:
                    writer.writerow({
                        'Customer ID': customer[0],
                        'Customer Name': customer[1],
                        'Address': customer[2],
                        'Status': customer[3],
                        'Notes': customer[4],
                        'Date Order': customer[5]
                    })

            print(f"Customer report generated: {output_file}")
        except sqlite3.Error as e:
            print(f"Error generating customer report: {e}")
        finally:
            self.disconnect()
