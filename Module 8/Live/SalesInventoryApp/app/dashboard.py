import customtkinter
import ttkbootstrap as ttkb
from tkinter import StringVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from app.backend import Backend  # Ensure this path is correct
import threading
import matplotlib

# Ensure the correct backend for matplotlib
matplotlib.use('TkAgg')


class DashboardScreen:
    def __init__(self, app):
        self.app = app

        # Dashboard content frame
        self.dashboard_frame = customtkinter.CTkFrame(
            self.app,
            corner_radius=15,
            border_width=0,
            fg_color="#ecf0f1"
        )
        self.dashboard_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Create the dashboard content
        self.create_dashboard_content()

    def fetch_highest_priced_orders(self):
        """Fetch and display the highest-priced orders dynamically."""
        backend = Backend()
        # Fetch highest priced orders
        return backend.get_highest_priced_orders()

    def create_dashboard_content(self):
        # Fetch highest-priced orders
        self.sales_data = self.fetch_highest_priced_orders()

        # Dashboard Header
        header_frame = customtkinter.CTkFrame(self.dashboard_frame, corner_radius=10, fg_color="#ecf0f1")
        header_frame.pack(fill="x", pady=10, padx=10)

        header_label = customtkinter.CTkLabel(
            header_frame,
            text="Sales Dashboard",
            font=("Verdana", 28, "bold"),
            text_color="#2c3e50"
        )
        header_label.pack()

        # Sales Data Table
        self.create_sales_table()

        # Detail View
        self.detail_frame = customtkinter.CTkFrame(self.dashboard_frame, corner_radius=10, fg_color="#ecf0f1")
        self.detail_frame.pack(pady=10, fill="both", expand=True, padx=10)

        self.detail_label = customtkinter.CTkLabel(
            self.detail_frame,
            text="Select an item to view details",
            font=("Verdana", 18),
            text_color="#2c3e50",
            wraplength=600,
            justify="left"
        )
        self.detail_label.pack(pady=20, padx=10)

        # Animated Graph
        self.graph_frame = customtkinter.CTkFrame(self.dashboard_frame, corner_radius=10, fg_color="#ecf0f1")
        self.graph_frame.pack(pady=10, fill="both", expand=True, padx=10)
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Bind table selection to update detail view and animated graph
        self.treeview.bind("<<TreeviewSelect>>", self.update_detail_view)

    def create_sales_table(self):
        sales_data_frame = customtkinter.CTkFrame(self.dashboard_frame, corner_radius=10, fg_color="#ecf0f1")
        sales_data_frame.pack(pady=10, fill="both", expand=True, padx=10)

        style = ttkb.Style()
        style.configure("Treeview", rowheight=25, font=("Verdana", 12))
        style.configure("Treeview.Heading", font=("Verdana", 14, "bold"))

        self.treeview = ttkb.Treeview(
            sales_data_frame,
            columns=("ID", "Item", "Ordered", "InStock", "Price"),
            show='headings',
            bootstyle="info"
        )
        self.treeview.heading("ID", text="Item ID")
        self.treeview.heading("Item", text="Item Name")
        self.treeview.heading("Ordered", text="Quantity Ordered")
        self.treeview.heading("InStock", text="In-Stock Quantity")
        self.treeview.heading("Price", text="Price ($)")

        self.treeview.column("ID", width=100, anchor="center")
        self.treeview.column("Item", width=200, anchor="w")
        self.treeview.column("Ordered", width=150, anchor="e")
        self.treeview.column("InStock", width=150, anchor="e")
        self.treeview.column("Price", width=150, anchor="e")

        # Populate table with sales data
        for row in self.sales_data:
            self.treeview.insert("", "end", values=row)

        self.treeview.pack(pady=(0, 0), fill="both", expand=True)

        # Add scrollbar
        scrollbar = ttkb.Scrollbar(
            sales_data_frame,
            orient="vertical",
            command=self.treeview.yview,
            bootstyle="info-round"
        )
        self.treeview.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def update_detail_view(self, event=None):
        selected_item = self.treeview.selection()
        if selected_item:
            item_data = self.treeview.item(selected_item, 'values')
            item_id = item_data[0]
            item_name = item_data[1]
            quantity_ordered = int(item_data[2])
            in_stock_quantity = int(item_data[3])
            price = float(item_data[4])

            detail_text = (
                f"Item ID: {item_id}\n"
                f"Item Name: {item_name}\n"
                f"Quantity Ordered: {quantity_ordered}\n"
                f"In-Stock Quantity: {in_stock_quantity}\n"
                f"Price: ${price:.2f}"
            )
            self.detail_label.configure(text=detail_text)

            # Update the graph
            self.update_animated_graph(quantity_ordered, in_stock_quantity)

    def update_animated_graph(self, ordered, in_stock):
        self.ax.clear()
        categories = ['Ordered', 'In Stock']
        values = [ordered, in_stock]
        self.ax.bar(categories, values, color=['blue', 'green'])
        self.ax.set_title("Stock vs Ordered Quantities", fontsize=16)
        self.ax.set_ylabel("Quantity")
        self.canvas.draw()
