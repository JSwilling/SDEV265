import customtkinter
from tkinter import messagebox

class ManageInventoryScreen:
    def __init__(self, app, backend):
        self.app = app
        self.backend = backend
        self.manage_frame = customtkinter.CTkFrame(self.app, corner_radius=15, border_width=3, border_color="#29487d")
        self.manage_frame.pack(side="right", fill="both", expand=True, padx=40, pady=20)

        # Title
        title_label = customtkinter.CTkLabel(self.manage_frame, text="Manage Inventory", font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="w")

        # Inventory Form (Left Side)
        customtkinter.CTkLabel(self.manage_frame, text="Item ID:").grid(row=1, column=0, padx=30, pady=5, sticky="w")
        self.item_id_entry = customtkinter.CTkEntry(self.manage_frame, width=300)
        self.item_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        customtkinter.CTkLabel(self.manage_frame, text="Product Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.product_entry = customtkinter.CTkEntry(self.manage_frame, width=300)
        self.product_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        customtkinter.CTkLabel(self.manage_frame, text="Size:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.size_entry = customtkinter.CTkEntry(self.manage_frame, width=300)
        self.size_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        customtkinter.CTkLabel(self.manage_frame, text="Quantity:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.quantity_entry = customtkinter.CTkEntry(self.manage_frame, width=300)
        self.quantity_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        customtkinter.CTkLabel(self.manage_frame, text="Price:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.price_entry = customtkinter.CTkEntry(self.manage_frame, width=300)
        self.price_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        # Submit, Update, Delete Buttons
        button_frame = customtkinter.CTkFrame(self.manage_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)

        submit_button = customtkinter.CTkButton(button_frame, text="Submit", command=self.submit_inventory, fg_color="#4267B2", hover_color="#3578E5")
        submit_button.pack(side="left", padx=15)

        update_button = customtkinter.CTkButton(button_frame, text="Update", command=self.update_inventory, fg_color="#4267B2", hover_color="#3578E5")
        update_button.pack(side="left", padx=15)

        delete_button = customtkinter.CTkButton(button_frame, text="Delete", command=self.delete_inventory, fg_color="#e74c3c", hover_color="#c0392b")
        delete_button.pack(side="left", padx=15)

        back_button = customtkinter.CTkButton(button_frame, text="Back", command=self.app.show_dashboard_screen, fg_color="#4267B2", hover_color="#3578E5")
        back_button.pack(side="left", padx=15)

    def submit_inventory(self):
        # Collect data from fields and save to backend
        data = {
            "item_id": self.item_id_entry.get(),
            "product": self.product_entry.get(),
            "size": self.size_entry.get(),
            "quantity": int(self.quantity_entry.get()),
            "price": float(self.price_entry.get())
        }
        self.backend.save_inventory(data)
        messagebox.showinfo("Success", "Inventory data saved successfully!")

    def update_inventory(self):
        # Collect data from fields and update in backend
        data = {
            "item_id": self.item_id_entry.get(),
            "product": self.product_entry.get(),
            "size": self.size_entry.get(),
            "quantity": int(self.quantity_entry.get()),
            "price": float(self.price_entry.get())
        }
        self.backend.save_inventory(data)
        messagebox.showinfo("Success", "Inventory data updated successfully!")

    def delete_inventory(self):
        # Delete inventory item by ID
        item_id = self.item_id_entry.get()
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete item ID: {item_id}?")
        if confirm:
            self.backend.connect()
            try:
                self.backend.cursor.execute('DELETE FROM items WHERE item_ID = ?', (item_id,))
                self.backend.conn.commit()
                messagebox.showinfo("Success", f"Item ID: {item_id} deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete item ID: {item_id}. Error: {e}")
            finally:
                self.backend.disconnect()



class Inventory:
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

    def create_item(self, product, size, quantity, price):
        """Create a new inventory item record in the items table."""
        self.connect()
        try:
            self.cursor.execute(
                '''INSERT INTO items (product, size, quantity, price) VALUES (?, ?, ?, ?)''',
                (product, size, quantity, price)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating item: {e}")
        finally:
            self.disconnect()

    def get_item(self, item_id=None):
        """Fetch inventory item data, optionally filtered by item ID."""
        self.connect()
        try:
            if item_id:
                self.cursor.execute('SELECT * FROM items WHERE item_ID = ?', (item_id,))
                return self.cursor.fetchone()
            else:
                self.cursor.execute('SELECT * FROM items')
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching items: {e}")
            return []
        finally:
            self.disconnect()

    def update_item(self, item_id, product, size, quantity, price):
        """Update an existing inventory item record."""
        self.connect()
        try:
            self.cursor.execute(
                '''UPDATE items SET product = ?, size = ?, quantity = ?, price = ? WHERE item_ID = ?''',
                (product, size, quantity, price, item_id)
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error updating item ID {item_id}: {e}")
        finally:
            self.disconnect()

    def delete_item(self, item_id):
        """Delete an inventory item from the items table."""
        self.connect()
        try:
            self.cursor.execute('DELETE FROM items WHERE item_ID = ?', (item_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error deleting item ID {item_id}: {e}")
        finally:
            self.disconnect()