import customtkinter
from tkinter import messagebox
from tkinter import ttk

class ManageInventoryScreen:
    def __init__(self, app, backend, user_role):
        self.app = app
        self.backend = backend
        self.user_role = user_role
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        self.main_frame = customtkinter.CTkFrame(self.app, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # Create Notebook for Tabs with enhanced styling
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 10], font=('Arial', 14, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#1ABC9C')], foreground=[('selected', 'white')])

        self.tab_control = ttk.Notebook(self.main_frame, style='TNotebook')
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=20)

        # Define Tabs
        self.orders_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15)
        self.sales_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15)
        self.items_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15)

        # Add Tabs to Notebook
        if self.user_role in ["Supervisor", "Salesperson", "Employee"]:
            self.tab_control.add(self.orders_tab, text='Orders')
            self.setup_orders_tab()
        if self.user_role in ["Salesperson"]:
            self.tab_control.add(self.sales_tab, text='Sales')
            self.setup_sales_tab()
        if self.user_role in ["Supervisor", "Salesperson", "Employee"]:
            self.tab_control.add(self.items_tab, text='Items')
            self.setup_items_tab()

    def setup_orders_tab(self):
        title_label = customtkinter.CTkLabel(self.orders_tab, text="Orders", font=("Arial", 24, "bold"), text_color="#2C3E50")
        title_label.pack(pady=20)

        # Search Bar for Orders
        search_frame = customtkinter.CTkFrame(self.orders_tab, corner_radius=10)
        search_frame.pack(fill="x", padx=10, pady=10)
        search_label = customtkinter.CTkLabel(search_frame, text="Search Orders:", font=("Arial", 14))
        search_label.pack(side="left", padx=10)
        self.search_entry_orders = customtkinter.CTkEntry(search_frame, width=300)
        self.search_entry_orders.pack(side="left", padx=10)
        search_button_orders = customtkinter.CTkButton(search_frame, text="Search", command=self.search_orders, fg_color="#1ABC9C", hover_color="#16A085")
        search_button_orders.pack(side="left", padx=10)

        # Placeholder for Order Display (Table)
        columns = ("Order Date", "Order ID", "Customer")
        self.order_table = ttk.Treeview(self.orders_tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.order_table.heading(col, text=col)
            self.order_table.column(col, width=200, anchor="center")
        self.order_table.pack(pady=10, padx=10, fill="both", expand=True)

        # Button to Add Orders (only for Supervisor and Salesperson)
        if self.user_role in ["Supervisor", "Salesperson"]:
            add_order_button = customtkinter.CTkButton(self.orders_tab, text="Add Order", command=self.add_order, fg_color="#007BFF", hover_color="#0056b3")
            add_order_button.pack(pady=10, side="bottom", anchor="center")

    def setup_sales_tab(self):
        title_label = customtkinter.CTkLabel(self.sales_tab, text="Create Sale", font=("Arial", 24, "bold"), text_color="#2C3E50")
        title_label.pack(pady=20)

        # Sales Form
        form_frame = customtkinter.CTkFrame(self.sales_tab, corner_radius=10)
        form_frame.pack(pady=10, padx=20, fill="x")

        customer_label = customtkinter.CTkLabel(form_frame, text="Customer Name:", font=("Arial", 14))
        customer_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.customer_entry = customtkinter.CTkEntry(form_frame, width=300)
        self.customer_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        item_id_label = customtkinter.CTkLabel(form_frame, text="Item ID:", font=("Arial", 14))
        item_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.item_id_entry = customtkinter.CTkEntry(form_frame, width=300)
        self.item_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        product_label = customtkinter.CTkLabel(form_frame, text="Product Name:", font=("Arial", 14))
        product_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.product_entry = customtkinter.CTkEntry(form_frame, width=300)
        self.product_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        quantity_label = customtkinter.CTkLabel(form_frame, text="Quantity:", font=("Arial", 14))
        quantity_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.quantity_entry = customtkinter.CTkEntry(form_frame, width=300)
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        price_label = customtkinter.CTkLabel(form_frame, text="Price per Unit:", font=("Arial", 14))
        price_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.price_entry = customtkinter.CTkEntry(form_frame, width=300)
        self.price_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        delivery_address_label = customtkinter.CTkLabel(form_frame, text="Delivery Address:", font=("Arial", 14))
        delivery_address_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.delivery_address_entry = customtkinter.CTkEntry(form_frame, width=300)
        self.delivery_address_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        contact_label = customtkinter.CTkLabel(form_frame, text="Contact Information:", font=("Arial", 14))
        contact_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.contact_entry = customtkinter.CTkEntry(form_frame, width=300)
        self.contact_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Notes Textbox
        notes_label = customtkinter.CTkLabel(form_frame, text="Notes:", font=("Arial", 14))
        notes_label.grid(row=7, column=0, padx=10, pady=5, sticky="nw")
        self.notes_textbox = customtkinter.CTkTextbox(form_frame, width=300, height=100)
        self.notes_textbox.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Button to Add Sale
        add_sale_button = customtkinter.CTkButton(self.sales_tab, text="Add Sale", command=self.add_sale, fg_color="#007BFF", hover_color="#0056b3")
        add_sale_button.pack(pady=20)

    def setup_items_tab(self):
        title_label = customtkinter.CTkLabel(self.items_tab, text="Manage Items", font=("Arial", 24, "bold"), text_color="#2C3E50")
        title_label.pack(pady=20)

        # Search Bar for Items
        search_frame = customtkinter.CTkFrame(self.items_tab, corner_radius=10)
        search_frame.pack(fill="x", padx=10, pady=10)
        search_label = customtkinter.CTkLabel(search_frame, text="Search Items:", font=("Arial", 14))
        search_label.pack(side="left", padx=10)
        self.search_entry_items = customtkinter.CTkEntry(search_frame, width=300)
        self.search_entry_items.pack(side="left", padx=10)
        search_button_items = customtkinter.CTkButton(search_frame, text="Search", command=self.search_items, fg_color="#1ABC9C", hover_color="#16A085")
        search_button_items.pack(side="left", padx=10)

        # Placeholder for Item Management (Table)
        columns = ("Item ID", "Product Name", "Size", "Quantity", "Price")
        self.item_table = ttk.Treeview(self.items_tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.item_table.heading(col, text=col)
            self.item_table.column(col, width=150, anchor="center")
        self.item_table.pack(pady=10, padx=10, fill="both", expand=True)

        # Button to Add Items (only for Supervisor)
        if self.user_role == "Supervisor":
            add_item_button = customtkinter.CTkButton(self.items_tab, text="Add Item", command=self.add_item, fg_color="#007BFF", hover_color="#0056b3")
            add_item_button.pack(pady=10, side="bottom", anchor="center")

    def add_order(self):
        # Placeholder for adding an order
        messagebox.showinfo("Add Order", "Functionality to add an order will go here.")

    def add_item(self):
        # Placeholder for adding an item
        messagebox.showinfo("Add Item", "Functionality to add an item will go here.")

    def add_sale(self):
        # Placeholder for adding a sale
        customer = self.customer_entry.get()
        item_id = self.item_id_entry.get()
        product = self.product_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        delivery_address = self.delivery_address_entry.get()
        contact = self.contact_entry.get()
        notes = self.notes_textbox.get("1.0", "end").strip()
        messagebox.showinfo("Add Sale", f"Sale added:\nCustomer: {customer}\nItem ID: {item_id}\nProduct: {product}\nQuantity: {quantity}\nPrice per Unit: {price}\nDelivery Address: {delivery_address}\nContact: {contact}\nNotes: {notes}")

    def search_orders(self):
        # Placeholder for searching orders
        search_term = self.search_entry_orders.get()
        messagebox.showinfo("Search Orders", f"Searching for orders with term: {search_term}")

    def search_items(self):
        # Placeholder for searching items
        search_term = self.search_entry_items.get()
        messagebox.showinfo("Search Items", f"Searching for items with term: {search_term}")

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

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

    def search_customer(self):
        # Placeholder for search customer logic
        pass

    def show_staff(self):
        # Placeholder for showing staff logic
        pass
