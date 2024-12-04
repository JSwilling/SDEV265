import customtkinter
from tkinter import messagebox
from tkinter import ttk
import tkinter.ttk as ttk

class ManageInventoryScreen:
    def __init__(self, app, backend, user_role):
        self.app = app
        self.backend = backend
        self.user_role = user_role
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
        title_label = customtkinter.CTkLabel(self.orders_tab, text="Orders", font=("Arial", 24, "bold"), text_color=title_color)
        title_label.pack(pady=20)

        # Search Bar for Orders
        search_frame = customtkinter.CTkFrame(self.orders_tab, corner_radius=10, fg_color=self.get_background_color())
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
        title_color = '#FFFFFF' if self.is_dark_mode else '#2C3E50'
        title_label = customtkinter.CTkLabel(self.sales_tab, text="Create Sale", font=("Arial", 24, "bold"), text_color=title_color)
        title_label.pack(pady=20)

        # Sales Form
        form_frame = customtkinter.CTkFrame(self.sales_tab, corner_radius=10, fg_color=self.get_background_color())
        form_frame.pack(pady=10, padx=20, fill="x")

        customer_label = customtkinter.CTkLabel(form_frame, text="Customer Name:", font=("Arial", 14))
        customer_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.customer_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(), text_color='#000000')
        self.customer_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        item_id_label = customtkinter.CTkLabel(form_frame, text="Item ID:", font=("Arial", 14))
        item_id_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.item_id_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(), text_color=self.get_entry_text_color())
        self.item_id_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        product_label = customtkinter.CTkLabel(form_frame, text="Product Name:", font=("Arial", 14))
        product_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.product_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(), text_color=self.get_entry_text_color())
        self.product_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        quantity_label = customtkinter.CTkLabel(form_frame, text="Quantity:", font=("Arial", 14))
        quantity_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.quantity_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(), text_color=self.get_entry_text_color())
        self.quantity_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        price_label = customtkinter.CTkLabel(form_frame, text="Price per Unit:", font=("Arial", 14))
        price_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.price_entry = customtkinter.CTkEntry(form_frame, width=300, fg_color=self.get_entry_background_color(), text_color=self.get_entry_text_color())
        self.price_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

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
        add_sale_button = customtkinter.CTkButton(self.sales_tab, text="Add Sale", command=self.add_sale, fg_color="#007BFF", hover_color="#0056b3")
        add_sale_button.pack(pady=20)

    def setup_items_tab(self):
        title_color = '#FFFFFF' if self.is_dark_mode else '#2C3E50'
        title_label = customtkinter.CTkLabel(self.items_tab, text="Manage Items", font=("Arial", 24, "bold"), text_color=title_color)
        title_label.pack(pady=20)

        # Search Bar for Items
        search_frame = customtkinter.CTkFrame(self.items_tab, corner_radius=10, fg_color=self.get_background_color())
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
        for tab, title in zip([self.orders_tab, self.sales_tab, self.items_tab], ["Orders", "Create Sale", "Manage Items"]):
            title_label = tab.winfo_children()[0]
            if isinstance(title_label, customtkinter.CTkLabel):
                title_label.configure(text_color=text_color)

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
        columns = ("Employee ID", "Name", "Position", "Team", "Office", "Country")
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
        # Placeholder function to load employee data - Replace this with actual backend call
        sample_employees = [
            ("E001", "John Doe", "UX Designer", "Design", "London", "United Kingdom"),
            ("E002", "Jane Smith", "Software Engineer", "Development", "New York", "United States"),
        ]
        for employee in sample_employees:
            self.employee_table.insert("", "end", values=employee)

    def show_employee_profile(self, event=None):
        # Open a popup to show employee details
        selected_item = self.employee_table.selection()
        if selected_item:
            employee_data = self.employee_table.item(selected_item, 'values')
            profile_window = customtkinter.CTkToplevel(self.app)
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
        # Placeholder function for terminating a user - Implement backend call here
        selected_item = self.employee_table.selection()
        if selected_item:
            employee_data = self.employee_table.item(selected_item, 'values')
            confirm = customtkinter.messagebox.askyesno("Confirm Termination", f"Are you sure you want to terminate {employee_data[1]}?")
            if confirm:
                # Here you would call your backend to terminate the user
                customtkinter.messagebox.showinfo("User Terminated", f"{employee_data[1]} has been terminated successfully.")

    def is_dark_mode(self):
        return customtkinter.get_appearance_mode() == "Dark"

    def get_background_color(self):
        return '#2C3E50' if self.is_dark_mode() else 'white'

def show_manage_staff_screen(app, backend, user_role):
    ManageStaffScreen(app, backend, user_role)
