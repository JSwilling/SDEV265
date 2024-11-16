import customtkinter
import ttkbootstrap as ttkb
from tkinter import StringVar
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
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
            fg_color="#ecf0f1"  # Light background color for dashboard content
        )
        self.dashboard_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Create the dashboard content
        self.create_dashboard_content()

    def create_dashboard_content(self):
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
        sales_data_frame = customtkinter.CTkFrame(self.dashboard_frame, corner_radius=10, fg_color="#ecf0f1")
        sales_data_frame.pack(pady=10, fill="both", expand=True, padx=10)

        # Generate simulated sales data
        self.generate_sales_data()

        style = ttkb.Style()  # Apply ttkbootstrap styling
        style.configure("Treeview", rowheight=25, font=("Verdana", 12))
        style.configure("Treeview.Heading", font=("Verdana", 14, "bold"))

        self.treeview = ttkb.Treeview(
            sales_data_frame,
            columns=("ID", "Item", "Quantity", "InHouse", "Price"),
            show='headings',
            bootstyle="info"
        )
        self.treeview.heading("ID", text="Item ID")
        self.treeview.heading("Item", text="Item Name")
        self.treeview.heading("Quantity", text="Quantity Ordered")
        self.treeview.heading("InHouse", text="In-house Quantity")
        self.treeview.heading("Price", text="Market Price ($)")

        self.treeview.column("ID", width=100, anchor="center")
        self.treeview.column("Item", width=200, anchor="w")
        self.treeview.column("Quantity", width=150, anchor="e")
        self.treeview.column("InHouse", width=150, anchor="e")
        self.treeview.column("Price", width=150, anchor="e")

        # Add sales data to treeview
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

        # Detail View Frame
        self.detail_frame = customtkinter.CTkFrame(self.dashboard_frame, corner_radius=10, fg_color="#ecf0f1")
        self.detail_frame.pack(pady=10, fill="both", expand=True, padx=10)
        self.detail_label = customtkinter.CTkLabel(
            self.detail_frame,
            text="Select an item to view details",
            font=("Verdana", 18),
            text_color="#2c3e50",
            wraplength=600,  # Ensure text wraps within the frame
            justify="left"   # Align text to the left
        )
        self.detail_label.pack(pady=20, padx=10)

        # Animated Graph Frame
        self.graph_frame = customtkinter.CTkFrame(self.dashboard_frame, corner_radius=10, fg_color="#ecf0f1")
        self.graph_frame.pack(pady=10, fill="both", expand=True, padx=10)
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Bind the selection event to update detail view and animated graph
        self.treeview.bind("<<TreeviewSelect>>", self.update_detail_view)

    def generate_sales_data(self):
        self.sales_data = []
        items = [
            "Apple iPhone 14 Pro", "Samsung Galaxy S22 Ultra", "Dell XPS 13 Laptop", "HP Envy Desktop PC",
            "ASUS ROG Strix Graphics Card", "LG UltraWide Monitor", "Logitech MX Master 3 Mouse",
            "Razer BlackWidow Keyboard", "Bose QuietComfort Headphones", "Google Nest Wifi Router",
            "Western Digital 2TB External HDD", "Canon EOS Rebel Camera", "Sony PlayStation 5 Console",
            "Microsoft Xbox Series X", "Amazon Echo Dot", "Apple MacBook Air", "Fitbit Charge 5 Smartwatch",
            "NVIDIA GeForce RTX 3080", "Apple AirPods Pro", "Samsung Galaxy Watch 5"
        ]
        for i in range(100):
            item_id = f"ITM-{1000 + i}"
            item_name = random.choice(items)
            quantity = random.randint(1, 500)
            in_house_quantity = random.randint(1, 1000)
            market_price = round(random.uniform(50, 1500), 2)
            self.sales_data.append((item_id, item_name, quantity, in_house_quantity, market_price))

    def update_detail_view(self, event=None):
        # Update detail view based on selected item from the table
        selected_item = self.treeview.selection()
        if selected_item:
            item_data = self.treeview.item(selected_item, 'values')
            item_id = item_data[0]
            item_name = item_data[1]
            quantity_ordered = int(item_data[2])
            in_house_quantity = int(item_data[3])
            market_price = float(item_data[4])
            in_demand = "Yes" if quantity_ordered / max(in_house_quantity, 1) > 0.5 else "No"

            # Additional details for fullscreen view
            if self.app.is_full_screen:
                product_description = (
                    f"{item_name} is a high-quality product designed to meet your needs. "
                    f"It is one of the best in the market, offering exceptional performance and value."
                )
                target_market = (
                    "Target Market: Tech enthusiasts, professionals, and general consumers looking for reliable products."
                )
                additional_info = f"Product Description: {product_description}\n{target_market}"
            else:
                additional_info = ""

            # Animated update for detail view
            self.animate_detail_view(
                item_id, item_name, quantity_ordered, in_house_quantity, market_price, in_demand, additional_info
            )

            # Update animated graph
            self.update_animated_graph(quantity_ordered, in_house_quantity)

    def animate_detail_view(self, item_id, item_name, quantity_ordered, in_house_quantity, market_price, in_demand, additional_info):
        # Clear previous detail text
        self.detail_label.configure(text="")

        # Create new detail text
        detail_text = (
            f"Item ID: {item_id}\n"
            f"Item Name: {item_name}\n"
            f"Quantity Ordered: {quantity_ordered}\n"
            f"In-house Quantity: {in_house_quantity}\n"
            f"Market Price: ${market_price:.2f}\n"
            f"In Demand: {in_demand}\n"
            f"{additional_info}"
        )

        # Animate typing effect
        def type_text(index=0):
            if index <= len(detail_text):
                self.detail_label.configure(
                    text=detail_text[:index],
                    font=("Courier", 16, "bold"),
                    text_color="#2c3e50"
                )
                self.app.after(20, lambda: type_text(index + 1))  # Adjust speed here

        type_text()

    def update_animated_graph(self, quantity_ordered, in_house_quantity):
        # Clear previous graph
        self.ax.clear()

        # Data for graph
        categories = ['Quantity Ordered', 'In-house Quantity']
        values = [quantity_ordered, in_house_quantity]

        # Animated bar chart
        bars = self.ax.bar(
            categories,
            [0, 0],
            color=['#3498db', '#2ecc71'],
            edgecolor='black',
            linewidth=0.7
        )
        self.ax.set_ylim(0, max(values) + 50)
        self.ax.set_title("Inventory Levels", fontsize=16, weight='bold', color="#34495e")
        self.ax.set_ylabel("Quantity", fontsize=12, color="#34495e")

        # Function to animate bars
        def animate_bars():
            for i in range(1, 101):
                for bar, value in zip(bars, values):
                    bar.set_height(value * (i / 100))
                self.canvas.draw()
                time.sleep(0.005)  # Adjust sleep time as needed

        threading.Thread(target=animate_bars).start()
