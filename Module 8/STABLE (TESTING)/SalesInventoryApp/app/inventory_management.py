import customtkinter
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.ttk as ttk
import sqlite3
import datetime


class Database:
    def __init__(self):
        self.db_path = r'db/Sales_Inventory.db'
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()


class ManageInventoryScreen:
    def __init__(self, app, backend, user_role, username):
        self.app = app
        self.backend = backend
        self.user_role = user_role
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        self.is_dark_mode = False
        # Main Frame
        self.main_frame = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color=self.get_background_color())
        self.main_frame.pack(fill="both", expand=True)

        # Create Notebook for Tabs with enhanced styling
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 10], font=('Arial', 14, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#1ABC9C')], foreground=[('selected', 'white')])

        self.tab_control = ttk.Notebook(self.main_frame, style='TNotebook')
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=20)

        # Define Tabs
        self.orders_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15, fg_color=self.get_background_color())
        self.sales_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15, fg_color=self.get_background_color())
        self.items_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15, fg_color=self.get_background_color())

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
        title_color = '#FFFFFF' if self.is_dark_mode else '#2C3E50'
        title_label = customtkinter.CTkLabel(self.orders_tab, text="Orders", font=("Arial", 24, "bold"),
                                             text_color=title_color)
        title_label.pack(pady=20)

        # Search Bar for Orders
        search_frame = customtkinter.CTkFrame(self.orders_tab, corner_radius=10, fg_color=self.get_background_color())
        search_frame.pack(fill="x", padx=10, pady=10)
        search_label = customtkinter.CTkLabel(search_frame, text="Search Orders:", font=("Arial", 14))
        search_label.pack(side="left", padx=10)
        self.search_entry_orders = customtkinter.CTkEntry(search_frame, width=300)
        self.search_entry_orders.pack(side="left", padx=10)
        search_button_orders = customtkinter.CTkButton(search_frame, text="Search", command=self.search_orders,
                                                       fg_color="#1ABC9C", hover_color="#16A085")
        search_button_orders.pack(side="left", padx=10)

        # Placeholder for Order Display (Table)
        columns = ("Order Date", "Order ID", "Customer")
        self.order_table = ttk.Treeview(self.orders_tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.order_table.heading(col, text=col)
            self.order_table.column(col, width=200, anchor="center")
        self.order_table.pack(pady=10, padx=10, fill="both", expand=True)

        # Control Panel for Supervisor
        if self.user_role == "Supervisor":
            control_frame = customtkinter.CTkFrame(self.orders_tab, corner_radius=10,
                                                   fg_color=self.get_background_color())
            control_frame.pack(fill="x", padx=10, pady=10)

            add_order_button = customtkinter.CTkButton(control_frame, text="Add Order", command=self.add_order,
                                                       fg_color="#007BFF", hover_color="#0056b3")
            add_order_button.pack(side="left", padx=10, pady=10)

            edit_order_button = customtkinter.CTkButton(control_frame, text="Edit Order", command=self.edit_order,
                                                        fg_color="#FFA500", hover_color="#FF8C00")
            edit_order_button.pack(side="left", padx=10, pady=10)

    def edit_order(self):
        selected_item = self.order_table.selection()
        if selected_item:
            order_details = self.order_table.item(selected_item, 'values')
            order_id = order_details[1]
            # Open a form to edit order details
            self.open_edit_order_form(order_id)

    def open_edit_order_form(self, order_id):
        db = Database()
        details = db.execute("""
            SELECT product, quantity, price, delivery_address, contact, notes, agent_id
            FROM Orders WHERE order_id = ?
        """, (order_id,))
        db.close()

        if details:
            details = details[0]
            popup = tk.Toplevel(self.app)
            popup.title(f"Edit Order - ID {order_id}")
            popup.geometry("450x700")  # Slightly larger dimensions
            popup.grab_set()

            # Create a frameless window
            popup.overrideredirect(True)
            popup.configure(bg='#f0f0f0')

            # Scrollable container
            canvas = tk.Canvas(popup, borderwidth=0, bg='#f0f0f0')
            frame = tk.Frame(canvas, bg='#f0f0f0')
            vsb = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=vsb.set)

            vsb.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((4, 4), window=frame, anchor="nw")

            frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

            # Editable fields with larger font
            entries = {}
            labels = ["Product", "Quantity", "Price", "Delivery Address", "Contact", "Agent ID"]
            for i, field in enumerate(labels):
                label = tk.Label(frame, text=f"{field}:", anchor='w', font=("Arial", 14, "bold"), bg='#f0f0f0')
                label.grid(row=i, column=0, sticky='w', pady=2, padx=10)
                entry = tk.Entry(frame, font=("Arial", 14), bg='#ffffff', width=35)
                entry.insert(0, details[i])
                entry.grid(row=i, column=1, sticky='w', pady=2, padx=10)
                entries[field] = entry

            # Notes editable text box
            notes_label = tk.Label(frame, text="Notes:", anchor='w', font=("Arial", 14, "bold"), bg='#f0f0f0')
            notes_label.grid(row=len(labels), column=0, sticky='w', pady=2, padx=10)
            notes_textbox = tk.Text(frame, height=5, width=40, font=("Arial", 12), bg='#ffffff')
            notes_textbox.insert("1.0", details[5])
            notes_textbox.grid(row=len(labels) + 1, column=0, columnspan=2, sticky="ew", padx=10, pady=2)

            # Submit and Cancel buttons
            submit_button = tk.Button(frame, text="Submit",
                                      command=lambda: self.submit_order_changes(order_id, entries, notes_textbox),
                                      font=("Arial", 14, "bold"), bg="#1ABC9C", fg="white")
            submit_button.grid(row=len(labels) + 2, column=0, pady=10, padx=10, sticky="ew")

            cancel_button = tk.Button(frame, text="Cancel", command=popup.destroy, font=("Arial", 14, "bold"),
                                      bg="#FF6347", fg="white")
            cancel_button.grid(row=len(labels) + 2, column=1, pady=10, padx=10, sticky="ew")

            # Make the window draggable
            def on_press(event):
                global xwin, ywin
                xwin = event.x
                ywin = event.y

            def on_drag(event):
                deltax = event.x - xwin
                deltay = event.y - ywin
                x = popup.winfo_x() + deltax
                y = popup.winfo_y() + deltay
                popup.geometry(f"+{x}+{y}")

            popup.bind('<ButtonPress-1>', on_press)
            popup.bind('<B1-Motion>', on_drag)

    def submit_order_changes(self, order_id, entries, notes_textbox):
        # Here, extract data from entries and update the database
        product = entries["Product"].get()
        quantity = entries["Quantity"].get()
        price = entries["Price"].get()
        delivery_address = entries["Delivery Address"].get()
        contact = entries["Contact"].get()
        agent_id = entries["Agent ID"].get()
        notes = notes_textbox.get("1.0", "end")

        db = Database()
        try:
            db.connect()
            db.execute("""
                UPDATE Orders SET product = ?, quantity = ?, price = ?, delivery_address = ?, contact = ?, notes = ?, agent_id = ?
                WHERE order_id = ?
            """, (product, quantity, price, delivery_address, contact, notes, agent_id, order_id))
            db.conn.commit()  # Commit changes to the database
            messagebox.showinfo("Success", "Order updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update order: {e}")
        finally:
            db.close()

    def setup_sales_tab(self):
        title_color = '#FFFFFF' if self.is_dark_mode else '#2C3E50'
        title_label = customtkinter.CTkLabel(self.sales_tab, text="Create Sale", font=("Arial", 24, "bold"),
                                             text_color=title_color)
        title_label.grid(row=0, columnspan=2, pady=20)
        self.sales_tab.grid_columnconfigure(0, weight=1)
        self.sales_tab.grid_columnconfigure(1, weight=1)

        form_frame = customtkinter.CTkFrame(self.sales_tab, corner_radius=10, fg_color=self.get_background_color())
        form_frame.grid(pady=10, padx=20, sticky="ew")

        # Configure grid layout to expand the last column
        form_frame.grid_columnconfigure(1, weight=1)

        customer_label = customtkinter.CTkLabel(form_frame, text="Customer Name:", font=("Arial", 14))
        customer_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.customer_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(),
                                                     text_color='#000000')
        self.customer_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        item_id_label = customtkinter.CTkLabel(form_frame, text="Item ID:", font=("Arial", 14))
        item_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.item_id_var = tk.StringVar()
        self.item_id_entry = customtkinter.CTkEntry(form_frame, textvariable=self.item_id_var, width=300,
                                                    fg_color=self.get_entry_background_color(),
                                                    text_color=self.get_entry_text_color())
        self.item_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.item_id_var.trace_add("write", lambda name, index, mode: self.update_product_name())
        self.item_id_var.trace_add("write", lambda name, index, mode: self.update_product_details())
        self.item_id_var.trace_add("write", self.update_product_details)  # Use self.update_product_details directly

        product_label = customtkinter.CTkLabel(form_frame, text="Product Name:", font=("Arial", 14))
        product_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.product_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color="grey",
                                                    text_color=self.get_entry_text_color(), state='readonly')
        self.product_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.product_entry.configure(fg_color="grey", state='readonly')
        quantity_label = customtkinter.CTkLabel(form_frame, text="Quantity:", font=("Arial", 14))
        quantity_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.quantity_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(), text_color=self.get_entry_text_color())
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        price_label = customtkinter.CTkLabel(form_frame, text="Price per Unit:", font=("Arial", 14))
        price_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        # Price per Unit Entry: only create one entry, set it as readonly and style it appropriately
        self.price_entry = customtkinter.CTkEntry(
            form_frame, width=300,
            fg_color="grey",  # Light grey background to indicate non-editability
            text_color=self.get_entry_text_color(),
            state='readonly'  # Make the field not editable
        )
        self.price_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        delivery_address_label = customtkinter.CTkLabel(form_frame, text="Delivery Address:", font=("Arial", 14))
        delivery_address_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.delivery_address_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(), text_color=self.get_entry_text_color())
        self.delivery_address_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        contact_label = customtkinter.CTkLabel(form_frame, text="Contact Information:", font=("Arial", 14))
        contact_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.contact_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(), text_color=self.get_entry_text_color())
        self.contact_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Notes Textbox
        notes_label = customtkinter.CTkLabel(form_frame, text="Notes:", font=("Arial", 14))
        notes_label.grid(row=7, column=0, padx=10, pady=5, sticky="nw")
        self.notes_textbox = customtkinter.CTkTextbox(form_frame, width=300, height=100, fg_color=self.get_entry_background_color(), text_color=self.get_entry_text_color())
        self.notes_textbox.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Button to Add Sale
        add_sale_button = customtkinter.CTkButton(self.sales_tab, text="Add Sale", command=self.add_sale,
                                                  fg_color="#007BFF", hover_color="#0056b3")
        add_sale_button.grid(row=10, column=0, columnspan=2, pady=20, padx=20,
                             sticky="ew")  # Adjust row according to your layout needs

    def update_product_name(self):
        item_id = self.item_id_var.get().strip()
        if item_id.isdigit():
            db = Database()
            cursor = db.connect()  # Ensure you're getting a cursor back correctly
            cursor.execute("SELECT Name FROM InventoryItem WHERE item_id = ?", (item_id,))
            product_name = cursor.fetchone()  # Fetch one result
            db.close()

            if product_name:
                self.product_entry.delete(0, 'end')
                self.product_entry.insert(0, product_name[0])  # Insert product name
            else:
                self.product_entry.delete(0, 'end')

    def update_product_details(self, *args):
        """Fetch and display product details based on the item ID."""
        item_id = self.item_id_var.get().strip()
        if item_id.isdigit():
            db = Database()
            try:
                cursor = db.connect()
                cursor.execute("SELECT Name, price FROM InventoryItem WHERE item_id = ?", (item_id,))
                result = cursor.fetchone()
                if result:
                    product_name, price = result
                    self.product_entry.configure(state='normal')  # Temporarily enable the field to update it
                    self.product_entry.delete(0, 'end')
                    self.product_entry.insert(0, product_name)
                    self.product_entry.configure(state='readonly')  # Set back to read-only

                    self.price_entry.configure(state='normal')  # Temporarily enable the field to update it
                    self.price_entry.delete(0, 'end')
                    self.price_entry.insert(0, price)
                    self.price_entry.configure(state='readonly')  # Set back to read-only
                else:
                    self.clear_product_and_price()
            finally:
                db.close()

    def setup_items_tab(self):
        # Determine text color based on dark mode status
        title_color = '#FFFFFF' if self.is_dark_mode else '#2C3E50'

        # Create a label for the tab title
        title_label = customtkinter.CTkLabel(self.items_tab, text="Manage Items", font=("Arial", 24, "bold"),
                                             text_color=title_color)
        title_label.pack(pady=20)

        # Setup the search frame for items
        search_frame = customtkinter.CTkFrame(self.items_tab, corner_radius=10, fg_color=self.get_background_color())
        search_frame.pack(fill="x", padx=10, pady=10)

        # Label for the search bar
        search_label = customtkinter.CTkLabel(search_frame, text="Search Items:", font=("Arial", 14))
        search_label.pack(side="left", padx=10)

        # Entry widget for search input
        self.search_entry_items = customtkinter.CTkEntry(search_frame, width=300)
        self.search_entry_items.pack(side="left", padx=10)

        # Button to trigger search
        search_button_items = customtkinter.CTkButton(search_frame, text="Search", command=self.search_items,
                                                      fg_color="#1ABC9C", hover_color="#16A085")
        search_button_items.pack(side="left", padx=10)

        # Setup the Treeview for item display
        columns = ("Item ID", "Product Name", "SKU#", "Price", "Quantity")
        self.item_table = ttk.Treeview(self.items_tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.item_table.heading(col, text=col)
            self.item_table.column(col, width=150, anchor="center")
        self.item_table.pack(pady=10, padx=10, fill="both", expand=True)

        # Add Item button for supervisors
        if self.user_role == "Supervisor":
            add_item_button = customtkinter.CTkButton(self.items_tab, text="Add Item", command=self.add_item,
                                                      fg_color="#007BFF", hover_color="#0056b3")
            add_item_button.pack(pady=10, side="bottom", anchor="center")

    def toggle_dark_mode(self):
        self.is_dark_mode = not self.is_dark_mode
        new_bg_color = self.get_background_color()
        new_entry_bg_color = self.get_entry_background_color()
        new_entry_text_color = self.get_entry_text_color()
        new_text_color = '#FFFFFF' if self.is_dark_mode else '#2C3E50'

        # Update main frame and tabs
        self.main_frame.configure(fg_color=new_bg_color)
        for tab in [self.orders_tab, self.sales_tab, self.items_tab]:
            tab.configure(fg_color=new_bg_color)
        self.update_tab_titles('#000000')

        # Update entries and textboxes
        for entry in [self.customer_entry, self.item_id_entry, self.product_entry, self.quantity_entry, self.price_entry, self.delivery_address_entry, self.contact_entry]:
            entry.configure(fg_color=new_entry_bg_color, text_color=new_entry_text_color)
        self.notes_textbox.configure(fg_color=new_entry_bg_color, text_color=new_entry_text_color)
        self.is_dark_mode = not self.is_dark_mode
        new_bg_color = self.get_background_color()
        new_text_color = '#FFFFFF' if self.is_dark_mode else '#2C3E50'
        self.main_frame.configure(fg_color=new_bg_color)
        for tab in [self.orders_tab, self.sales_tab, self.items_tab]:
            tab.configure(fg_color=new_bg_color)
        self.update_tab_titles(new_text_color)

    def get_background_color(self):
        return '#2C3E50' if self.is_dark_mode else 'white'

    def get_entry_background_color(self):
        return '#3E4C59' if self.is_dark_mode else '#FFFFFF'

    def get_entry_text_color(self):
        return '#FFFFFF' if self.is_dark_mode else '#000000'
        return '#2C3E50' if self.is_dark_mode else 'white'

    def update_tab_titles(self, text_color):
        for tab, title in zip([self.orders_tab, self.sales_tab, self.items_tab],
                              ["Orders", "Create Sale", "Manage Items"]):
            if tab.winfo_exists():
                title_label = tab.winfo_children()[0]
                if isinstance(title_label, customtkinter.CTkLabel) and title_label.winfo_exists():
                    title_label.configure(text_color=text_color)

    def add_order(self):
        # Create a popup for adding a new order
        popup = tk.Toplevel(self.app)
        popup.title("Add New Order")
        popup.geometry("450x700")
        popup.grab_set()

        # Frameless window configuration
        popup.overrideredirect(True)
        popup.configure(bg='#f0f0f0')

        # Scrollable container
        canvas = tk.Canvas(popup, borderwidth=0, bg='#f0f0f0')
        frame = tk.Frame(canvas, bg='#f0f0f0')
        vsb = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # Entry fields setup
        entry_fields = {
            "Customer Name": None,
            "Item ID": None,
            "Product Name": None,
            "Quantity": None,
            "Price": None,
            "Delivery Address": None,
            "Contact Information": None,
            "Agent ID": None,
            "Notes": None,
        }

        for i, label in enumerate(entry_fields.keys()):
            tk.Label(frame, text=f"{label}:", anchor='w', font=("Arial", 14, "bold"), bg='#f0f0f0').grid(row=i,
                                                                                                         column=0,
                                                                                                         sticky='w',
                                                                                                         pady=2,
                                                                                                         padx=10)
            if label == "Notes":
                entry = tk.Text(frame, height=5, width=40, font=("Arial", 12), bg='#ffffff')
            else:
                entry = tk.Entry(frame, font=("Arial", 14), bg='#ffffff', width=35)
            entry.grid(row=i, column=1, sticky='w', pady=2, padx=10)
            entry_fields[label] = entry

        # Pre-fill Agent ID for convenience, but allow editing
        entry_fields["Agent ID"].insert(0, self.username)

        # Submit Button
        submit_button = tk.Button(frame, text="Submit Order", command=lambda: self.submit_order_to_db(entry_fields),
                                  font=("Arial", 14, "bold"), bg="#1ABC9C", fg="white")
        submit_button.grid(row=len(entry_fields), column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Cancel Button
        cancel_button = tk.Button(frame, text="Cancel", command=popup.destroy, font=("Arial", 14, "bold"), bg="#FF6347",
                                  fg="white")
        cancel_button.grid(row=len(entry_fields) + 1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Make the window draggable
        def on_press(event):
            global xwin, ywin
            xwin = event.x
            ywin = event.y

        def on_drag(event):
            deltax = event.x - xwin
            deltay = event.y - ywin
            x = popup.winfo_x() + deltax
            y = popup.winfo_y() + deltay
            popup.geometry(f"+{x}+{y}")

        popup.bind('<ButtonPress-1>', on_press)
        popup.bind('<B1-Motion>', on_drag)

    def submit_order_to_db(self, entry_fields):
        try:
            # Extract data from entry fields
            customer_name = entry_fields["Customer Name"].get()
            item_id = entry_fields["Item ID"].get()
            product_name = entry_fields["Product Name"].get()
            quantity = int(entry_fields["Quantity"].get())
            price = float(entry_fields["Price"].get())
            delivery_address = entry_fields["Delivery Address"].get()
            contact_info = entry_fields["Contact Information"].get()
            agent_id = entry_fields["Agent ID"].get()
            notes = entry_fields["Notes"].get("1.0", "end").strip()

            # Append admin creation note to the notes field
            notes += f"\n(Note: Order created by Admin {self.username} on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})"

            # Insert order into the database
            order_date = datetime.datetime.now().strftime("%Y-%m-%d")
            db = Database()
            cursor = db.connect()

            # Ensure the Orders table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_date TEXT NOT NULL,
                    customer TEXT NOT NULL,
                    item_id TEXT NOT NULL,
                    product TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    delivery_address TEXT,
                    contact TEXT,
                    notes TEXT,
                    agent_id TEXT NOT NULL
                );
            """)

            # Insert the new order
            cursor.execute("""
                INSERT INTO Orders (order_date, customer, item_id, product, quantity, price, delivery_address, contact, notes, agent_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (order_date, customer_name, item_id, product_name, quantity, price, delivery_address, contact_info, notes, agent_id))

            db.conn.commit()  # Commit changes to the database
            db.close()

            messagebox.showinfo("Success", "Order added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add order: {e}")


    def add_item(self):
        # Ensure all required widgets are initialized
        self.add_item_popup()

    def add_item_popup(self):
        popup = tk.Toplevel(self.app)
        popup.title("Add New Inventory Item")
        popup.geometry("450x700")  # Slightly larger dimensions
        popup.grab_set()

        # Create a frameless window
        popup.overrideredirect(True)
        popup.configure(bg='#f0f0f0')

        # Scrollable container
        canvas = tk.Canvas(popup, borderwidth=0, bg='#f0f0f0')
        frame = tk.Frame(canvas, bg='#f0f0f0')
        vsb = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4, 4), window=frame, anchor="nw")

        frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # Entry fields setup
        entry_fields = {
            "Item Name": None,
            "SKU": None,
            "Price": None,
            "Stock Level": None
        }

        for i, label in enumerate(entry_fields.keys()):
            tk.Label(frame, text=f"{label}:", anchor='w', font=("Arial", 14, "bold"), bg='#f0f0f0').grid(row=i,
                                                                                                         column=0,
                                                                                                         sticky='w',
                                                                                                         pady=2,
                                                                                                         padx=10)
            entry = tk.Entry(frame, font=("Arial", 14), bg='#ffffff', width=35)
            entry.grid(row=i, column=1, sticky='w', pady=2, padx=10)
            entry_fields[label] = entry

        # Submit Button
        submit_button = tk.Button(frame, text="Add Item", command=lambda: self.submit_item_to_db(entry_fields),
                                  font=("Arial", 14, "bold"), bg="#1ABC9C", fg="white")
        submit_button.grid(row=len(entry_fields), column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Cancel Button
        cancel_button = tk.Button(frame, text="Cancel", command=popup.destroy, font=("Arial", 14, "bold"), bg="#FF6347",
                                  fg="white")
        cancel_button.grid(row=len(entry_fields) + 1, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Make the window draggable
        def on_press(event):
            global xwin, ywin
            xwin = event.x
            ywin = event.y

        def on_drag(event):
            deltax = event.x - xwin
            deltay = event.y - ywin
            x = popup.winfo_x() + deltax
            y = popup.winfo_y() + deltay
            popup.geometry(f"+{x}+{y}")

        popup.bind('<ButtonPress-1>', on_press)
        popup.bind('<B1-Motion>', on_drag)

    def submit_item_to_db(self, entry_fields):
        product = entry_fields["Item Name"].get()
        sku = entry_fields["SKU"].get()
        price = float(entry_fields["Price"].get())
        stock_level = int(entry_fields["Stock Level"].get())

        db = Database()
        try:
            db.connect()
            db.execute("INSERT INTO InventoryItem (Name, SKU, price, stockLevel) VALUES (?, ?, ?, ?)",
                       (product, sku, price, stock_level))
            db.conn.commit()
            messagebox.showinfo("Success", "Item added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {e}")
        finally:
            db.close()

    def add_sale(self):
        customer = self.customer_entry.get()
        item_id = self.item_id_entry.get()
        product = self.product_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        delivery_address = self.delivery_address_entry.get()
        contact = self.contact_entry.get()
        notes = self.notes_textbox.get("1.0", "end").strip()
        agent_id = self.username  # Ensure this is correctly set upon initializing the instance
        order_date = datetime.datetime.now().strftime("%Y-%m-%d")

        db = Database()
        try:
            cursor = db.connect()
            # Ensure the Orders table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Orders (
                    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_date TEXT,
                    customer TEXT,
                    item_id TEXT,
                    product TEXT,
                    quantity INTEGER,
                    price REAL,
                    delivery_address TEXT,
                    contact TEXT,
                    notes TEXT,
                    agent_id TEXT
                );
            """)
            # Insert the new sale
            cursor.execute("""
                INSERT INTO Orders (order_date, customer, item_id, product, quantity, price, delivery_address, contact, notes, agent_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (order_date, customer, item_id, product, quantity, price, delivery_address, contact, notes, agent_id))
            db.conn.commit()  # Ensure changes are committed to the database
            messagebox.showinfo("Add Sale", "Sale added successfully.")
            self.clear_sale_form()  # Clear the form
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add sale: {e}")
        finally:
            db.close()

    def search_orders(self):
        search_term = self.search_entry_orders.get()
        db = Database()
        query = """
            SELECT order_date, order_id, customer FROM Orders 
            WHERE customer LIKE ? OR order_id LIKE ?
            ORDER BY order_date DESC
        """
        # Use '%' wildcards to allow partial matches
        results = db.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
        db.close()

        # Clear existing entries in the table
        for i in self.order_table.get_children():
            self.order_table.delete(i)

        # Insert new results into the table
        for row in results:
            self.order_table.insert('', 'end', values=row)

        # Add a binding to the table for click events
        self.order_table.bind("<Double-1>", self.on_order_click)

    def on_order_click(self, event):
        item = self.order_table.selection()[0]
        order_details = self.order_table.item(item, 'values')
        order_id = order_details[1]

        db = Database()
        details = db.execute("""
            SELECT product, quantity, price, delivery_address, contact, notes, agent_id
            FROM Orders WHERE order_id = ?
        """, (order_id,))
        db.close()

        if details:
            details = details[0]
            popup = tk.Toplevel(self.app)
            popup.title(f"Order Details - ID {order_id}")
            popup.geometry("450x700")  # Slightly larger dimensions
            popup.grab_set()

            # Create a frameless window
            popup.overrideredirect(True)
            popup.configure(bg='#f0f0f0')

            # Scrollable container
            canvas = tk.Canvas(popup, borderwidth=0, bg='#f0f0f0')
            frame = tk.Frame(canvas, bg='#f0f0f0')
            vsb = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=vsb.set)

            vsb.pack(side="right", fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            canvas.create_window((4, 4), window=frame, anchor="nw")

            frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

            # Data display with larger font
            labels = {
                "Order ID": order_id,
                "Product": details[0],
                "Quantity": details[1],
                "Price": f"${details[2]}",
                "Delivery Address": details[3],
                "Contact": details[4],
                "Agent ID": details[6]
            }

            for i, (label_text, value) in enumerate(labels.items()):
                label = tk.Label(frame, text=f"{label_text}:", anchor='w', font=("Arial", 14, "bold"), bg='#f0f0f0')
                value_label = tk.Label(frame, text=value, anchor='w', font=("Arial", 14), bg='#f0f0f0')
                label.grid(row=i, column=0, sticky='w', pady=2, padx=10)
                value_label.grid(row=i, column=1, sticky='w', pady=2, padx=10)

            # Notes display
            notes_label = tk.Label(frame, text="Notes:", anchor='w', font=("Arial", 14, "bold"), bg='#f0f0f0')
            notes_label.grid(row=len(labels), column=0, sticky='w', pady=2, padx=10)
            notes_textbox = tk.Text(frame, height=5, width=40, font=("Arial", 12), bg='#f0f0f0')
            notes_textbox.grid(row=len(labels) + 1, column=0, columnspan=2, sticky="ew", padx=10, pady=2)
            notes_textbox.insert("1.0", details[5])

            # Close button
            close_button = tk.Button(frame, text="Close", command=popup.destroy, font=("Arial", 14, "bold"),
                                     bg="#1ABC9C", fg="white")
            close_button.grid(row=len(labels) + 2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

            # Make the window draggable
            def on_press(event):
                global xwin, ywin
                xwin = event.x
                ywin = event.y

            def on_drag(event):
                deltax = event.x - xwin
                deltay = event.y - ywin
                x = popup.winfo_x() + deltax
                y = popup.winfo_y() + deltay
                popup.geometry(f"+{x}+{y}")

            popup.bind('<ButtonPress-1>', on_press)
            popup.bind('<B1-Motion>', on_drag)

    def search_items(self):
        search_term = self.search_entry_items.get()
        db = Database()
        try:
            cursor = db.connect()
            cursor.execute("SELECT * FROM InventoryItem WHERE Name LIKE ?", ('%' + search_term + '%',))
            items = cursor.fetchall()
            for i in self.item_table.get_children():
                self.item_table.delete(i)
            for item in items:
                self.item_table.insert('', 'end', values=item)
        finally:
            db.close()

    def clear_content_frame(self):
        if hasattr(self, 'content_frame') and self.content_frame.winfo_exists():
            for widget in self.content_frame.winfo_children():
                if widget.winfo_exists():
                    widget.destroy()

    def clear_product_and_price(self):
        """Clears the product name and price fields."""
        self.product_entry.configure(state='normal')
        self.product_entry.delete(0, 'end')
        self.product_entry.configure(state='readonly')

        self.price_entry.configure(state='normal')
        self.price_entry.delete(0, 'end')
        self.price_entry.configure(state='readonly')

    def clear_sale_form(self):
        self.customer_entry.delete(0, 'end')
        self.item_id_entry.delete(0, 'end')
        self.product_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.delivery_address_entry.delete(0, 'end')
        self.contact_entry.delete(0, 'end')
        self.notes_textbox.delete("1.0", "end")


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
        item_id = self.item_id_entry.get()
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete item ID: {item_id}?")
        if confirm and self.item_id_entry.winfo_exists():
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


class ManageStaffScreen:
    def __init__(self, app, backend, user_role):
        self.app = app
        self.backend = backend
        self.user_role = user_role
        self.setup_ui()

    def setup_ui(self):
        # Main Frame
        self.main_frame = customtkinter.CTkFrame(self.app, corner_radius=0, fg_color=self.get_background_color())
        self.main_frame.pack(fill="both", expand=True)

        # Create Notebook for Tabs with enhanced styling
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[10, 10], font=('Arial', 14, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#1ABC9C')], foreground=[('selected', 'white')])

        self.tab_control = ttk.Notebook(self.main_frame, style='TNotebook')
        self.tab_control.pack(expand=1, fill="both", padx=20, pady=20)

        # Define Tabs
        self.employees_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15, fg_color=self.get_background_color())
        self.manage_tab = customtkinter.CTkFrame(self.tab_control, corner_radius=15, fg_color=self.get_background_color())

        # Add Tabs to Notebook
        self.tab_control.add(self.employees_tab, text='Employees')
        self.setup_employees_tab()

        self.tab_control.add(self.manage_tab, text='Manage')
        self.setup_manage_tab()

    def setup_employees_tab(self):
        title_color = '#FFFFFF' if self.is_dark_mode() else '#2C3E50'
        title_label = customtkinter.CTkLabel(self.employees_tab, text="Employees", font=("Arial", 24, "bold"), text_color=title_color)
        title_label.pack(pady=20)

        # Placeholder for Employee Table (TreeView)
        columns = ("Username", "Position")
        self.employee_table = ttk.Treeview(self.employees_tab, columns=columns, show="headings", height=10)
        for col in columns:
            self.employee_table.heading(col, text=col)
            self.employee_table.column(col, width=150, anchor="center")
        self.employee_table.pack(pady=10, padx=10, fill="both", expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.employees_tab, orient="vertical", command=self.employee_table.yview)
        self.employee_table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Load employee data
        self.load_employees()

        # Bind employee selection to open profile
        self.employee_table.bind("<<TreeviewSelect>>", self.show_employee_profile)

    def setup_manage_tab(self):
        title_color = '#FFFFFF' if self.is_dark_mode() else '#2C3E50'
        title_label = customtkinter.CTkLabel(self.manage_tab, text="Manage Staff", font=("Arial", 24, "bold"), text_color=title_color)
        title_label.pack(pady=20)

        # Terminate User Button
        terminate_user_button = customtkinter.CTkButton(
            self.manage_tab, text="Terminate User", command=self.terminate_user, fg_color="#FF4C4C", hover_color="#FF1C1C", text_color="#ffffff"
        )
        terminate_user_button.pack(pady=10)

        # Placeholder for other management options
        # You can add additional buttons and forms here to manage staff members

    def load_employees(self):
        # Connect to the database
        db_path = r'db/Sales_Inventory.db'
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Query to get all users
        cursor.execute("SELECT username, role FROM users;")
        users = cursor.fetchall()

        # Insert users into the table
        for user in users:
            self.employee_table.insert("", "end", values=user)

        # Close the database connection
        connection.close()

    def show_employee_profile(self, event=None):
        selected_item = self.employee_table.selection()
        if selected_item and self.employee_table.winfo_exists():
            employee_data = self.employee_table.item(selected_item, 'values')
            profile_window = customtkinter.CTkToplevel(self.app)
            if profile_window.winfo_exists():  # Checking the existence of the new window
                profile_window.title("Employee Profile")
                profile_window.geometry("400x400")

            # Header
            profile_label = customtkinter.CTkLabel(profile_window, text="Employee Profile", font=("Arial", 20, "bold"), fg_color="#1ABC9C", text_color="#ffffff")
            profile_label.pack(pady=20)

            # Display Employee Details
            details_text = f"Employee ID: {employee_data[0]}\nName: {employee_data[1]}\nPosition: {employee_data[2]}\nTeam: {employee_data[3]}\nOffice: {employee_data[4]}\nCountry: {employee_data[5]}"
            details_label = customtkinter.CTkLabel(profile_window, text=details_text, font=("Arial", 16), text_color="#34495e", wraplength=350)
            details_label.pack(pady=20, padx=10)

            # Back button
            back_button = customtkinter.CTkButton(profile_window, text="Close", command=profile_window.destroy, width=160, height=50, corner_radius=10, fg_color="#1abc9c", hover_color="#16a085", text_color="#ffffff")
            back_button.pack(pady=20)

    def terminate_user(self):
        selected_item = self.employee_table.selection()
        if selected_item:
            employee_data = self.employee_table.item(selected_item, 'values')
            username = employee_data[0]  # Assuming the username is in the first column
            confirm = messagebox.askyesno(
                "Confirm Termination",
                f"Are you sure you want to terminate {username}?"
            )
            if confirm:
                try:
                    # Connect to the database
                    db_path = r'Mdb/Sales_Inventory.db'
                    connection = sqlite3.connect(db_path)
                    cursor = connection.cursor()

                    # Delete the user from the database
                    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
                    connection.commit()

                    # Remove the user from the table view
                    self.employee_table.delete(selected_item)

                    messagebox.showinfo("Success", f"User {username} has been terminated successfully.")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to terminate user: {e}")
                finally:
                    connection.close()
    def is_dark_mode(self):
        return customtkinter.get_appearance_mode() == "Dark"

    def get_background_color(self):
        return '#2C3E50' if self.is_dark_mode() else 'white'

def show_manage_staff_screen(app, backend, user_role):
    ManageStaffScreen(app, backend, user_role)
