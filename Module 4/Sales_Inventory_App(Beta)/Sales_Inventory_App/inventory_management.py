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

        customtkinter.CTkLabel(self.manage_frame, text="Order ID:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.order_id_entry = customtkinter.CTkEntry(self.manage_frame, width=300)
        self.order_id_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        customtkinter.CTkLabel(self.manage_frame, text="Customer Name:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.customer_name_entry = customtkinter.CTkEntry(self.manage_frame, width=300)
        self.customer_name_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        customtkinter.CTkLabel(self.manage_frame, text="Address:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.address_entry = customtkinter.CTkEntry(self.manage_frame, width=300)
        self.address_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Radio Buttons for Status
        status_frame = customtkinter.CTkFrame(self.manage_frame)
        status_frame.grid(row=5, column=0, columnspan=2, pady=10, sticky="w")

        self.status_var = customtkinter.StringVar(value="")
        status_label = customtkinter.CTkLabel(status_frame, text="Status:")
        status_label.grid(row=0, column=0, padx=10)

        self.pending_radio = customtkinter.CTkRadioButton(status_frame, text="Pending", variable=self.status_var, value="Pending", command=self.toggle_radio)
        self.pending_radio.grid(row=0, column=1, padx=10)

        self.shipped_radio = customtkinter.CTkRadioButton(status_frame, text="Shipped", variable=self.status_var, value="Shipped", command=self.toggle_radio)
        self.shipped_radio.grid(row=0, column=2, padx=10)

        self.returned_radio = customtkinter.CTkRadioButton(status_frame, text="Returned", variable=self.status_var, value="Returned", command=self.toggle_radio)
        self.returned_radio.grid(row=0, column=3, padx=10)

        # Quantity increment/decrement buttons
        quantity_frame = customtkinter.CTkFrame(self.manage_frame)
        quantity_frame.grid(row=6, column=0, columnspan=2, pady=10, sticky="w")

        customtkinter.CTkLabel(quantity_frame, text="Quantity:").grid(row=0, column=0, padx=10)
        self.quantity_value = customtkinter.IntVar(value=0)
        quantity_display = customtkinter.CTkLabel(quantity_frame, textvariable=self.quantity_value)
        quantity_display.grid(row=0, column=1, padx=10)

        increment_button = customtkinter.CTkButton(quantity_frame, text="+", command=lambda: self.adjust_quantity(1))
        increment_button.grid(row=0, column=2, padx=10)

        decrement_button = customtkinter.CTkButton(quantity_frame, text="-", command=lambda: self.adjust_quantity(-1))
        decrement_button.grid(row=0, column=3, padx=10)

        # Notes Section (Right Side)
        notes_label = customtkinter.CTkLabel(self.manage_frame, text="Notes:")
        notes_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        self.notes_textbox = customtkinter.CTkTextbox(self.manage_frame, width=300, height=200)
        self.notes_textbox.grid(row=2, column=2, rowspan=4, padx=10, pady=5, sticky="nw")

        # Submit, Search, and Back Buttons
        button_frame = customtkinter.CTkFrame(self.manage_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=20)

        submit_button = customtkinter.CTkButton(button_frame, text="Submit", command=self.submit_inventory, fg_color="#4267B2", hover_color="#3578E5")
        submit_button.pack(side="left", padx=15)

        search_button = customtkinter.CTkButton(button_frame, text="Search", command=self.search_inventory, fg_color="#4267B2", hover_color="#3578E5")
        search_button.pack(side="left", padx=15)

        back_button = customtkinter.CTkButton(button_frame, text="Back", command=self.app.show_dashboard_screen, fg_color="#4267B2", hover_color="#3578E5")
        back_button.pack(side="left", padx=15)

    def toggle_radio(self):
        current_value = self.status_var.get()
        if current_value == self.pending_radio.cget("value"):
            self.status_var.set("")

    def adjust_quantity(self, amount):
        new_value = self.quantity_value.get() + amount
        if new_value >= 0:
            self.quantity_value.set(new_value)

    def submit_inventory(self):
        # Collect data from fields and save to backend
        data = {
            "item_id": self.item_id_entry.get(),
            "order_id": self.order_id_entry.get(),
            "customer_name": self.customer_name_entry.get(),
            "address": self.address_entry.get(),
            "status": self.status_var.get(),
            "quantity": self.quantity_value.get(),
            "notes": self.notes_textbox.get("1.0", "end").strip()
        }
        self.backend.save_inventory(data)
        messagebox.showinfo("Success", "Inventory data saved successfully!")

    def search_inventory(self):
        # Search backend for the item_id and display the result
        item_id = self.item_id_entry.get()
        result = self.backend.query_inventory(item_id)
        if result:
            formatted_result = f"Item ID: {result['item_id']}\nOrder ID: {result['order_id']}\nCustomer Name: {result['customer_name']}\nAddress: {result['address']}\nStatus: {result['status']}\nQuantity: {result['quantity']}\nNotes: {result['notes']}"
            messagebox.showinfo("Search Result", formatted_result)
        else:
            messagebox.showwarning("Not Found", "No inventory data found for the given Item ID.")